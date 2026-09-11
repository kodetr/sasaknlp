"""Production normalizer for Bahasa Sasak texts."""

from __future__ import annotations

import re
import string
from typing import Optional

from sasaknlp.core.config import NormalizerConfig
from sasaknlp.normalization.rules import (
    clean_control_characters,
    collapse_whitespace,
    normalize_diacritics,
    normalize_quotes_and_apostrophes,
    normalize_unicode,
)


class SasakNormalizer:
    """Normalizes raw Bahasa Sasak text for downstream NLP processing.

    Handles Unicode canonicalization, glottal stop apostrophes, whitespace
    tidying, and configurable casefolding or punctuation removal.
    """

    def __init__(self, config: Optional[NormalizerConfig] = None) -> None:
        self.config = config or NormalizerConfig()
        # Create punctuation removal translator if needed, but preserve apostrophes and hyphens
        # if preserve_hyphenated_words is True
        punct = string.punctuation
        if self.config.preserve_hyphenated_words:
            punct = punct.replace("-", "")
        # Always preserve apostrophe because of glottal stops in Sasak orthography
        punct = punct.replace("'", "")
        self._punct_regex = re.compile(f"[{re.escape(punct)}]")

    def normalize(self, text: str) -> str:
        """Run full normalization pipeline on text string."""
        if not text:
            return ""

        # Step 1: Clean control characters
        cleaned = clean_control_characters(text)

        # Step 2: Unicode normalization (NFC)
        cleaned = normalize_unicode(cleaned, form=self.config.unicode_form)

        # Step 3: Quotes and apostrophes
        if self.config.normalize_quotes:
            cleaned = normalize_quotes_and_apostrophes(cleaned)

        # Step 3b: Normalize regional diacritics
        cleaned = normalize_diacritics(cleaned)

        # Step 4: Lowercase if enabled
        if self.config.lowercase:
            cleaned = cleaned.lower()

        # Step 5: Optional punctuation removal
        if self.config.strip_punctuation:
            cleaned = self._punct_regex.sub(" ", cleaned)

        # Step 6: Collapse whitespace
        if self.config.remove_extra_whitespace:
            cleaned = collapse_whitespace(cleaned)

        return cleaned

    def normalize_word(self, word: str) -> str:
        """Normalize a single token or word, stripping surrounding punctuation."""
        if not word:
            return ""
        norm = self.normalize(word)
        # Strip leading/trailing non-alphanumeric punctuation except glottal apostrophe
        norm = re.sub(r"^[^a-zA-Z0-9']+", "", norm)
        norm = re.sub(r"[^a-zA-Z0-9']+$", "", norm)
        return norm
