"""Stopwords (kata tugas) filtering and management for Bahasa Sasak.

Provides corpus-verified functional words (prepositions, conjunctions, pronouns,
particles, negation, question words, and dialect-specific markers) for text
classification, information retrieval, and downstream NLP tasks.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, Set, Union


class SasakStopwords:
    """Manages and filters stopwords for Bahasa Sasak.

    Supports cross-dialectal standard stopwords and dialect-specific markers
    (e.g., Selaparang/Menu-Meni, Ngeno-Ngene, Mriak-Mriku, Kramak/Alus).
    """

    _DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "stopwords_sasak.json"

    def __init__(
        self,
        custom_stopwords: Optional[Iterable[str]] = None,
        dialect: Optional[str] = None,
        data_path: Optional[Union[str, Path]] = None,
    ) -> None:
        self.data_path = Path(data_path) if data_path else self._DEFAULT_DATA_PATH
        self.categories: Dict[str, List[str]] = {}
        self.dialect_specific: Dict[str, List[str]] = {}
        self._base_stopwords: Set[str] = set()

        self._load_data()

        self.dialect = dialect
        if custom_stopwords:
            self._base_stopwords.update(w.strip().lower() for w in custom_stopwords if w.strip())

    def _load_data(self) -> None:
        """Load stopwords from JSON definition file."""
        if not self.data_path.exists():
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.categories = data.get("categories", {})
        self.dialect_specific = data.get("dialect_specific", {})

        for words in self.categories.values():
            self._base_stopwords.update(w.lower() for w in words)

    def get_stopwords(
        self,
        dialect: Optional[str] = None,
        include_dialect: bool = True,
    ) -> Set[str]:
        """Return a set of Sasak stopwords.

        Args:
            dialect: Specific dialect name (e.g., 'selaparang', 'ngeno_ngene',
                     'mriak_mriku', 'kramak_alus').
            include_dialect: If True and dialect is None, includes markers from
                             all dialects. If False, returns only core cross-dialectal
                             stopwords.

        Returns:
            Set of lowercase stopword strings.
        """
        target_dialect = dialect or self.dialect
        result = set(self._base_stopwords)

        if target_dialect:
            # Add specific dialect markers
            if target_dialect in self.dialect_specific:
                result.update(w.lower() for w in self.dialect_specific[target_dialect])
        elif include_dialect:
            # Include all dialect markers
            for dialect_words in self.dialect_specific.values():
                result.update(w.lower() for w in dialect_words)

        return result

    def is_stopword(self, word: str, dialect: Optional[str] = None) -> bool:
        """Check if a given word is a Sasak stopword."""
        if not word:
            return False
        clean_word = word.strip().lower()
        return clean_word in self.get_stopwords(dialect=dialect)

    def add(self, words: Union[str, Iterable[str]]) -> None:
        """Add one or more custom words to the stopword dictionary."""
        if isinstance(words, str):
            words = [words]
        for w in words:
            if w and w.strip():
                self._base_stopwords.add(w.strip().lower())

    def remove(self, words: Union[str, Iterable[str]]) -> None:
        """Remove one or more words from the base stopword dictionary."""
        if isinstance(words, str):
            words = [words]
        for w in words:
            clean_w = w.strip().lower()
            self._base_stopwords.discard(clean_w)
            for d_words in self.dialect_specific.values():
                if clean_w in d_words:
                    d_words.remove(clean_w)

    def filter_tokens(
        self,
        tokens: List[str],
        dialect: Optional[str] = None,
    ) -> List[str]:
        """Filter out stopwords from a list of tokens.

        Args:
            tokens: List of token strings.
            dialect: Optional dialect context.

        Returns:
            Filtered list of tokens preserving non-stopwords and order.
        """
        stopwords_set = self.get_stopwords(dialect=dialect)
        return [tok for tok in tokens if tok.lower() not in stopwords_set]

    def filter_text(
        self,
        text: str,
        dialect: Optional[str] = None,
    ) -> str:
        """Remove stopwords from a raw text string, returning cleaned string."""
        if not text:
            return ""

        # Simple regex tokenizer preserving words with hyphens and glottal stops
        tokens = re.findall(r"\b[a-zA-Z0-9'-]+\b|[^\w\s]", text)
        filtered = self.filter_tokens(tokens, dialect=dialect)
        return " ".join(filtered)


# Default module-level instance
_DEFAULT_INSTANCE: Optional[SasakStopwords] = None


def _get_default_instance() -> SasakStopwords:
    global _DEFAULT_INSTANCE
    if _DEFAULT_INSTANCE is None:
        _DEFAULT_INSTANCE = SasakStopwords()
    return _DEFAULT_INSTANCE


def get_stopwords(
    dialect: Optional[str] = None,
    include_dialect: bool = True,
) -> Set[str]:
    """Retrieve Sasak stopwords set.

    Usage:
        >>> from sasaknlp.stopwords import get_stopwords
        >>> stops = get_stopwords()
        >>> 'dait' in stops
        True
    """
    return _get_default_instance().get_stopwords(
        dialect=dialect,
        include_dialect=include_dialect,
    )


def remove_stopwords(
    text_or_tokens: Union[str, List[str]],
    dialect: Optional[str] = None,
) -> Union[str, List[str]]:
    """Remove Sasak stopwords from a text string or list of tokens.

    Usage:
        >>> from sasaknlp import remove_stopwords
        >>> remove_stopwords("tiang mangan nasiq leq bale")
        'mangan nasiq bale'
        >>> remove_stopwords(['tiang', 'mangan', 'leq', 'bale'])
        ['mangan', 'bale']
    """
    instance = _get_default_instance()
    if isinstance(text_or_tokens, list):
        return instance.filter_tokens(text_or_tokens, dialect=dialect)
    return instance.filter_text(text_or_tokens, dialect=dialect)


def is_stopword(word: str, dialect: Optional[str] = None) -> bool:
    """Check if a word is a Sasak stopword."""
    return _get_default_instance().is_stopword(word, dialect=dialect)


__all__ = [
    "SasakStopwords",
    "get_stopwords",
    "remove_stopwords",
    "is_stopword",
]
