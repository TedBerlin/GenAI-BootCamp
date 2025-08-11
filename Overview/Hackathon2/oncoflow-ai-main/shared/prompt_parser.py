from typing import Dict, Any
import re

# ---------------- PROMPT PARSING ----------------
def parse_guidance(guidance: str) -> Dict[str, Any]:
    if not guidance:
        return {"topics": [], "word_limit": None, "format": None}

    g = guidance.lower()

    # Topics
    topic_patterns = [
        r'focus on ([^.;\n]+)',
        r'about ([^.;\n]+)',
        r'on the topics? of ([^.;\n]+)',
        r'regarding ([^.;\n]+)',
        r'summarize ([^.;\n]+)'
    ]

    topics = []
    for pattern in topic_patterns:
        m = re.search(pattern, g)
        if m:
            raw = m.group(1)
            topics += [t.strip() for t in re.split(r',| and ', raw) if t.strip()]
    topics = list(set(topics))  # unique

    # Word limit
    word_limit_patterns = [
        r'(\d+)\s*-\s*word',
        r'(\d+)\s*word',
        r'limit .* to (\d+) words',
        r'around (\d+) words',
        r'about (\d+) words',
    ]

    word_limit = None
    for pattern in word_limit_patterns:
        m = re.search(pattern, g)
        if m:
            word_limit = int(m.group(1))
            break

    # Format
    format_map = {
        'bullet': 'bullets',
        'bulleted': 'bullets',
        'itemized': 'bullets',
        'list': 'bullets',
        'numbered': 'numbered',
        'ordered': 'numbered',
        'abstract': 'abstract',
        'json': 'json'
    }

    fmt = None
    for k, v in format_map.items():
        if k in g:
            fmt = v
            break

    return {"topics": topics, "word_limit": word_limit, "format": fmt}