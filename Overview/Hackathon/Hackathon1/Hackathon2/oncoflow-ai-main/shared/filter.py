from sentence_transformers import SentenceTransformer
import faiss
from typing import List
from shared.utils import get_device

# ---------------- SEMANTIC FILTERING ----------------
class SemanticFilter:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.device = get_device()
        self.model = SentenceTransformer(model_name, device=str(self.device))
        self.index = None
        self.chunks: List[str] = []

    def build(self, chunks: List[str]):
        self.chunks = chunks
        embeddings = self.model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def filter_by_topics(self, topics: List[str], top_k: int = 5) -> List[str]:
        if not topics or not self.index:
            return self.chunks
        query = " ".join(topics)
        q_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, idxs = self.index.search(q_emb, top_k)
        return [self.chunks[i] for i in idxs[0]]