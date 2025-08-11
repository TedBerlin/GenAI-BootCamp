import re

# ---------------- CLEANING ----------------
def clean_text(text: str) -> str:
    text = re.sub(r'-+\s*Advertisement\s*-+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Sorry,.*?(video player!|download it.*?player!)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F\uFFFD]', ' ', text)
    text = re.sub(r'(?m)^(Page\s+\d+.*)$', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def aggressive_clean(text: str) -> str:
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?]) +', text)
    keep = [
        s for s in sentences
        if not re.search(
            r'(advertisement|subscribe|browser|video player|read more|friends)',
            s, flags=re.IGNORECASE
        )
    ]
    return ' '.join(keep)