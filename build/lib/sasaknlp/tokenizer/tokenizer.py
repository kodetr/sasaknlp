"""Word and token-level tokenizer for Bahasa Sasak."""

from __future__ import annotations

import re
from typing import List, Pattern, Tuple


class SasakTokenizer:
    """Tokenizer designed for Bahasa Sasak morphological characteristics.

    Preserves reduplicated word constructs (e.g., 'bareng-bareng', 'pinaq-pinaq')
    and glottal-stop apostrophes (e.g., 'sa\'iq', 'tepina\''), while cleanly
    handling punctuation tokens.
    """

    # Pattern matches:
    # 1. Words with hyphens (reduplications like bareng-bareng)
    # 2. Words with glottal apostrophes (sa'iq, manuk')
    # 3. Numbers with decimals (12.5)
    # 4. Standard words
    # 5. Individual punctuation marks
    TOKEN_REGEX: Pattern[str] = re.compile(
        r"""
        [a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)*(?:-[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)*)+  # Reduplications / hyphenated
        | [a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)*'?                                    # Words with internal/trailing glottal stop
        | '\w+                                                                # Words with leading apostrophe
        | \d+(?:[.,]\d+)+                                                     # Numbers with decimals
        | \d+                                                                 # Integers
        | [^\w\s]                                                             # Punctuation characters
        """,
        re.VERBOSE,
    )

    WORD_ONLY_REGEX: Pattern[str] = re.compile(
        r"^[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)*(?:-[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)*)*'?$"
    )

    def __init__(self, preserve_case: bool = True) -> None:
        self.preserve_case = preserve_case

    def tokenize(self, text: str, keep_punct: bool = False) -> List[str]:
        """Tokenize text into a list of word/symbol tokens.

        Args:
            text: Input string to tokenize.
            keep_punct: If True, retains standalone punctuation tokens;
                        if False, discards non-word punctuation tokens.

        Returns:
            List of token strings.
        """
        if not text:
            return []

        raw_tokens = self.TOKEN_REGEX.findall(text)
        tokens: List[str] = []

        for tok in raw_tokens:
            tok_str = tok if self.preserve_case else tok.lower()
            if keep_punct:
                tokens.append(tok_str)
            else:
                # Keep if contains alphanumeric characters
                if any(c.isalnum() for c in tok_str):
                    tokens.append(tok_str)

        return tokens

    def span_tokenize(self, text: str, keep_punct: bool = False) -> List[Tuple[str, int, int]]:
        """Tokenize text and return token string along with (start_char, end_char) spans."""
        if not text:
            return []

        spans: List[Tuple[str, int, int]] = []
        for match in self.TOKEN_REGEX.finditer(text):
            tok = match.group()
            start, end = match.span()
            if keep_punct or any(c.isalnum() for c in tok):
                tok_str = tok if self.preserve_case else tok.lower()
                spans.append((tok_str, start, end))

        return spans
