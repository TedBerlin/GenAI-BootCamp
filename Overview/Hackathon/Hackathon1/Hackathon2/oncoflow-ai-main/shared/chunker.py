from typing import List

# ---------------- CHUNKING ----------------
def chunk_by_words(text: str, max_words: int = 300, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    step = max_words - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + max_words])
        if chunk:
            chunks.append(chunk)
    return chunks