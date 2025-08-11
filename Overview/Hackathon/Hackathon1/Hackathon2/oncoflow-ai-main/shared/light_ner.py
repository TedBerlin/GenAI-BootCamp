import spacy
from typing import Dict
import re

# ---------------- ENTITY FIND & RESTORE ----------------
# (Strict: only replace full n-grams present in the summary, case-insensitive)
_spacy_nlp = None
def _get_spacy():
    global _spacy_nlp
    if _spacy_nlp is None:
        _spacy_nlp = spacy.load("en_core_web_sm")
    return _spacy_nlp

def find_entities(text: str) -> Dict[str, str]:
    nlp = _get_spacy()
    doc = nlp(text)
    entities: Dict[str, str] = {}
    for ent in doc.ents:
        norm = ent.text.lower()
        if norm not in entities:
            entities[norm] = ent.text  # preserve original casing of first occurrence
    return entities

def restore_entities(summary: str, entities: Dict[str, str]) -> str:
    if not entities:
        return summary

    def replacement(match):
        found = match.group(0)
        return entities.get(found.lower(), found)

    # sort longer first to avoid partial overlaps
    sorted_entities = sorted(entities.keys(), key=len, reverse=True)
    pattern = r'\b(' + '|'.join(re.escape(e) for e in sorted_entities) + r')\b'
    return re.sub(pattern, replacement, summary, flags=re.IGNORECASE)