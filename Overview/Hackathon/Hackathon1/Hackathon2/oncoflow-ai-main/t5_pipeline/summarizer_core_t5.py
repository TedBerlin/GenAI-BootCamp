import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import shared.cleaner as cleaner
from shared.utils import get_device
from shared.cleaner import aggressive_clean
from shared.utils import get_device
from shared.prompt_parser import parse_guidance
from shared.light_ner import find_entities, restore_entities
from shared.chunker import chunk_by_words
from shared.filter import SemanticFilter
from shared.post_processor import enforce_word_limit, apply_format, fix_spacing_and_capitalization

device = get_device()

# ---------------- SUMMARIZER ----------------
class Summarizer:
    def __init__(self, model_name: str = "t5-small"):
        hf_device = 0 if device.type in ("cuda", "mps") else -1
        self.pipe = pipeline("summarization", model=model_name, tokenizer=model_name, device=hf_device)

    def summarize_text(self, text: str, guidance: Optional[str] = None) -> str:
        spec = parse_guidance(guidance) if guidance else {"topics": [], "word_limit": None, "format": None}

        # clean & entity inventory
        cleaned = cleaner.aggressive_clean(text)
        entities = find_entities(cleaned)

        # chunk
        chunks = chunk_by_words(cleaned, max_words=300, overlap=50)

        # semantic filtering
        if spec["topics"]:
            sf = SemanticFilter()
            sf.build(chunks)
            chunks = sf.filter_by_topics(spec["topics"], top_k=5)

        # summarize chunks
        partial_summaries = []
        for ch in chunks:
            if len(ch.split()) < 30:
                continue
            s = self.pipe(ch, max_length=100, do_sample=False)[0]["summary_text"]
            partial_summaries.append(s)

        if not partial_summaries:
            return "No meaningful content found."

        # final synthesis
        joined = " ".join(partial_summaries)
        summary = self.pipe(joined, max_length=120, do_sample=False)[0]["summary_text"]

        # restore entities, formatting
        summary = restore_entities(summary, entities)
        summary = enforce_word_limit(summary, spec["word_limit"])
        summary = apply_format(summary, spec["format"])
        summary = fix_spacing_and_capitalization(summary)

        return summary
    
    def summarize_multiple_texts(self, texts: List[str], guidance: Optional[str] = None) -> str:
        spec = parse_guidance(guidance) if guidance else {"topics": [], "word_limit": None, "format": None}

        # Clean and chunk all texts
        all_chunks = []
        all_entities = {}
        for text in texts:
            cleaned = aggressive_clean(text)
            entities = find_entities(cleaned)
            all_entities.update(entities)
            all_chunks.extend(chunk_by_words(cleaned, max_words=300, overlap=50))

        # Semantic filtering
        if spec["topics"]:
            sf = SemanticFilter()
            sf.build(all_chunks)
            all_chunks = sf.filter_by_topics(spec["topics"], top_k=5)

        # Summarize chunks
        partial_summaries = []
        for ch in all_chunks:
            if len(ch.split()) < 30:
                continue
            s = self.pipe(ch, max_length=100, do_sample=False)[0]["summary_text"]
            partial_summaries.append(s)

        if not partial_summaries:
            return "No meaningful content found."

        # Final synthesis
        joined = " ".join(partial_summaries)
        summary = self.pipe(joined, max_length=120, do_sample=False)[0]["summary_text"]

        # Restore entities and apply formatting
        summary = restore_entities(summary, all_entities)
        summary = enforce_word_limit(summary, spec["word_limit"])
        summary = apply_format(summary, spec["format"])
        summary = fix_spacing_and_capitalization(summary)

        return summary

# ---------------- RETRIEVER (for eval script) ----------------
class Retriever:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name, device=str(device))
        self.index = None
        self.passages: List[str] = []

    def build(self, passages: List[str]):
        self.passages = passages
        embs = self.model.encode(passages, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        dim = embs.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embs)

    def search(self, query: str, top_k: int = 10) -> List[int]:
        q = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, idxs = self.index.search(q, top_k)
        return idxs[0].tolist()
