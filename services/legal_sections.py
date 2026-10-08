"""Identify actual article headings, not cross-references."""
from __future__ import annotations
import re

ARTICLE_HEADING = re.compile(r"^[ \t]*Article[ \t]+(\d+[a-z]?)[ \t]*$", re.I | re.M)
ANNEX_HEADING = re.compile(r"^[ \t]*ANNEX[ \t]+[IVXLCDM]+[ \t]*$", re.M)
ARTICLE_QUERY = re.compile(r"(?<![a-z])(?:articles?|art\.?)[ \t]*(\d+[a-z]?)(?![\da-z])|第\s*(\d+[a-z]?)\s*条", re.I)

def requested_articles(question: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys((m.group(1) or m.group(2)).lower()
                              for m in ARTICLE_QUERY.finditer(question)))

def article_units(text: str, current: str | None):
    """Carry headings across pages and end articles at the next heading/annex."""
    # EUR-Lex running headers are page labels, not continuation text.
    text = re.sub(r"^[ \t]*\d{5}R\d+[^\n]*[—–][^\n]*$", "", text, flags=re.M)
    text = re.sub(r"^[ \t]*▼[A-Z]\d*[ \t]*$", "", text, flags=re.M)
    boundaries = sorted(
        [(m.start(), m.group(1).lower()) for m in ARTICLE_HEADING.finditer(text)]
        + [(m.start(), None) for m in ANNEX_HEADING.finditer(text)]
    )
    units = []
    start = 0
    for position, article in boundaries:
        prefix = text[start:position].strip()
        if prefix:
            units.append((prefix, current))
        current = article
        start = position
    remainder = text[start:].strip()
    if remainder:
        units.append((remainder, current))
    return units, current
