"""Text normalization rules and string transformations for Bahasa Sasak."""

from __future__ import annotations

import re
import unicodedata
from typing import Pattern

# Unicode quote and apostrophe variants commonly occurring in regional texts
APOSTROPHE_MAP = {
    "\u2018": "'",  # Left single quotation mark
    "\u2019": "'",  # Right single quotation mark
    "\u02BC": "'",  # Modifier letter apostrophe (used for glottal stop)
    "\u02BD": "'",  # Modifier letter reversed comma
    "\u201B": "'",  # Single high-reversed-9 quotation mark
    "`": "'",       # Grave accent sometimes used as apostrophe
    "´": "'",       # Acute accent
}

QUOTE_MAP = {
    "\u201C": '"',  # Left double quotation mark
    "\u201D": '"',  # Right double quotation mark
    "\u00AB": '"',  # Left-pointing double angle quotation mark
    "\u00BB": '"',  # Right-pointing double angle quotation mark
}

# Regex to collapse multiple whitespace characters into a single space
RE_MULTI_WHITESPACE: Pattern[str] = re.compile(r"\s+")

# Regex to remove non-printable / control characters (except standard newline/tab)
RE_CONTROL_CHARS: Pattern[str] = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")


# Mapping for Sasak regional Latin diacritics to standard orthography
DIACRITIC_MAP = {
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "á": "a", "à": "a", "â": "a", "ä": "a",
    "ó": "o", "ò": "o", "ö": "o", "ô": "o",
    "ú": "u", "ù": "u", "ü": "u", "û": "u",
    "í": "i", "ì": "i", "ï": "i", "î": "i",
    "É": "E", "È": "E", "Ê": "E", "Ë": "E",
    "Á": "A", "À": "A", "Â": "A", "Ä": "A",
    "Ó": "O", "Ò": "O", "Ö": "O", "Ô": "O",
    "Ú": "U", "Ù": "U", "Ü": "U", "Û": "U",
    "Í": "I", "Ì": "I", "Ï": "I", "Î": "I",
}


def normalize_diacritics(text: str) -> str:
    """Standardize regional Sasak diacritics (é, è, â, ó) to standard Latin vowels."""
    for old, new in DIACRITIC_MAP.items():
        text = text.replace(old, new)
    return text


def normalize_unicode(text: str, form: str = "NFC") -> str:
    """Normalize unicode characters to a standard representation form."""
    return unicodedata.normalize(form, text)


def normalize_quotes_and_apostrophes(text: str) -> str:
    """Standardize curly quotes and apostrophes to ASCII equivalents.

    Crucial for Bahasa Sasak because apostrophes are frequently used to represent
    phonological glottal stops (e.g. sa'iq, manuk').
    """
    for old, new in APOSTROPHE_MAP.items():
        text = text.replace(old, new)
    for old, new in QUOTE_MAP.items():
        text = text.replace(old, new)
    return text


def clean_control_characters(text: str) -> str:
    """Remove non-printable control characters."""
    return RE_CONTROL_CHARS.sub("", text)


def collapse_whitespace(text: str) -> str:
    """Collapse consecutive spaces/newlines into a single space and strip boundaries."""
    return RE_MULTI_WHITESPACE.sub(" ", text).strip()

