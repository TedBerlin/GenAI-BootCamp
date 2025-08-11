from typing import Optional
import re

# ---------------- POST-PROCESSING ----------------
def enforce_word_limit(summary: str, word_limit: Optional[int]) -> str:
    if not word_limit or word_limit <= 0:
        return summary
    words = summary.split()
    return " ".join(words[:word_limit])

def to_bullets(summary: str) -> str:
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
    return "\n".join(f"• {s}" for s in sentences)

def to_numbered(summary: str) -> str:
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))

def to_abstract(summary: str) -> str:
    return f"**Abstract** — {summary}"

def to_json(summary: str) -> str:
    import json
    return json.dumps({"summary": summary}, ensure_ascii=False, indent=2)

def apply_format(summary: str, fmt: Optional[str]) -> str:
    if fmt == "bullets":
        return to_bullets(summary)
    if fmt == "numbered":
        return to_numbered(summary)
    if fmt == "abstract":
        return to_abstract(summary)
    if fmt == "json":
        return to_json(summary)
    return summary

def fix_spacing_and_capitalization(text: str) -> str:
    # remove extra space before punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    # capitalize sentence starts
    parts = re.split(r'([.!?]\s+)', text)
    out = []
    for i in range(0, len(parts), 2):
        s = parts[i].strip()
        if s:
            s = s[0].upper() + s[1:]
            out.append(s)
        if i + 1 < len(parts):
            out.append(parts[i + 1])
    return ''.join(out).strip()