import subprocess
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import faiss
from shared.cleaner import aggressive_clean
from shared.utils import get_device
from shared.prompt_parser import parse_guidance
from shared.light_ner import find_entities, restore_entities
from shared.chunker import chunk_by_words
from shared.filter import SemanticFilter
from shared.post_processor import enforce_word_limit, apply_format, fix_spacing_and_capitalization

device = get_device()

# ---------------- OLLAMA RUN WRAPPER ----------------
def ollama_summarize(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3:mini"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error calling Ollama: {e}"


# ---------------- SUMMARIZER ----------------
class Summarizer:
    def __init__(self):
        pass  # no HF pipeline needed

    def summarize_text(self, text: str, guidance: Optional[str] = None) -> str:
        spec = parse_guidance(guidance or "")
        cleaned = aggressive_clean(text)
        entities = find_entities(cleaned)
        chunks = chunk_by_words(cleaned, max_words=300, overlap=50)

        if spec["topics"]:
            sf = SemanticFilter()
            sf.build(chunks)
            chunks = sf.filter_by_topics(spec["topics"], top_k=5)

        partial_summaries = []
        for ch in chunks:
            if len(ch.split()) < 30:
                continue
            if guidance:
                prompt = f"{guidance}\n\nSummarize this text clearly and concisely:\n\n{ch}"
            else:
                prompt = f"Summarize this text clearly and concisely:\n\n{ch}"
            s = ollama_summarize(prompt)
            partial_summaries.append(s)

        if not partial_summaries:
            return "No meaningful content found."

        joined = " ".join(partial_summaries)
        if guidance:
            prompt = f"{guidance}\n\nSummarize this text clearly and concisely:\n\n{joined}"
        else:
            prompt = f"Summarize this text clearly and concisely:\n\n{joined}"
        summary = ollama_summarize(prompt)

        summary = restore_entities(summary, entities)
        summary = enforce_word_limit(summary, spec["word_limit"])
        summary = apply_format(summary, spec["format"])
        summary = fix_spacing_and_capitalization(summary)

        return summary



# ---------------- EXAMPLE USAGE ----------------
if __name__ == "__main__":
    example_text = (
        "OpenAI's ChatGPT has revolutionized natural language processing. "
        "It can summarize, translate, and generate text with impressive accuracy. "
        "Many industries are now adopting this technology to improve workflows."
    )
    guidance = "Focus on natural language processing and keep it under 50 words in bullet points."
    summarizer = Summarizer()
    result = summarizer.summarize_text(example_text, guidance)
    print(result)

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
