"""Sentence boundary detection for Sasak texts with honorific and abbreviation protection."""

from __future__ import annotations

import re
from typing import List, Pattern, Set

# Regional nobility titles, religious titles, and common Indonesian/Sasak abbreviations
DEFAULT_ABBREVIATIONS: Set[str] = {
    "tgh",    # Tuan Guru Haji
    "tg",     # Tuan Guru
    "l",      # Lalu (Sasak male nobility)
    "b",      # Baiq (Sasak female nobility)
    "raden",  # Raden
    "r",      # Raden
    "h",      # Haji
    "hj",     # Hajjah
    "dr",     # Doctor
    "drs",    # Dokteranda
    "prof",   # Professor
    "ir",     # Insinyur
    "ust",    # Ustadz
    "dll",    # Dan lain-lain
    "dsb",    # Dan sebagainya
    "dst",    # Dan seterusnya
    "no",     # Nomor
    "jl",     # Jalan
}


class SasakSentenceTokenizer:
    """Sentence boundary detector respecting Sasak regional abbreviations and titles."""

    # Sentence terminal punctuation (. ! ?) followed by whitespace or end of string
    SENTENCE_SPLIT_REGEX: Pattern[str] = re.compile(r"([.!?]+)(?:\s+|$)")

    def __init__(self, custom_abbreviations: Set[str] | None = None) -> None:
        self.abbreviations = set(DEFAULT_ABBREVIATIONS)
        if custom_abbreviations:
            self.abbreviations.update(a.lower() for a in custom_abbreviations)

    def tokenize(self, text: str) -> List[str]:
        """Split text into sentences while guarding against false sentence boundaries."""
        if not text or not text.strip():
            return []

        text = text.strip()
        sentences: List[str] = []
        current_sentence: List[str] = []

        tokens = text.split()
        for i, token in enumerate(tokens):
            current_sentence.append(token)

            # Check if token ends with sentence terminator
            match = re.search(r"([.!?]+)$", token)
            if match:
                term = match.group(1)
                bare = token[:-len(term)].lower()

                # Check if this token is a known abbreviation (e.g. "Tgh.", "L.")
                if term == "." and bare in self.abbreviations:
                    # Do not split on abbreviation
                    continue

                # Check if it looks like a single capital letter abbreviation (e.g. "A.")
                if term == "." and len(bare) == 1 and bare.isalpha():
                    continue

                # Check if followed by lowercase word in same paragraph (often continuation)
                if i + 1 < len(tokens) and tokens[i + 1][0].islower():
                    continue

                # Otherwise boundary confirmed
                sentences.append(" ".join(current_sentence))
                current_sentence = []

        if current_sentence:
            sentences.append(" ".join(current_sentence))

        return [s.strip() for s in sentences if s.strip()]
