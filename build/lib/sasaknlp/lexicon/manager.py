"""Manager for SasakLex dictionary with efficient lookups, trie indexing, and dialect querying."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from sasaknlp.core.types import LexiconEntry
from sasaknlp.lexicon.loader import LexiconLoader
from sasaknlp.lexicon.trie import PrefixTrie

DEFAULT_LEXICON_PATH = Path(__file__).parent / "data" / "sasaklex.json"


class SasakLexManager:
    """Manages the SasakLex lexicon in memory with O(1) hash indexing and Trie-based prefix lookup."""

    def __init__(self, data_path: Optional[Union[str, Path]] = None, auto_load_default: bool = True) -> None:
        self._entries_by_word: Dict[str, LexiconEntry] = {}
        self._entries_by_lemma: Dict[str, List[LexiconEntry]] = {}
        self._entries_by_dialect: Dict[str, List[LexiconEntry]] = {}
        self._trie = PrefixTrie()

        if data_path:
            self.load(data_path)
        elif auto_load_default and DEFAULT_LEXICON_PATH.exists():
            self.load(DEFAULT_LEXICON_PATH)

    def load(self, path: Union[str, Path]) -> None:
        """Load lexicon data from JSON or CSV into the manager."""
        p = Path(path)
        if p.suffix.lower() == ".csv":
            entries = LexiconLoader.load_from_csv(p)
        else:
            entries = LexiconLoader.load_from_json(p)

        for entry in entries:
            self.add_entry(entry)

    def add_entry(self, entry: LexiconEntry) -> None:
        """Add or update an individual lexicon entry in the indexes."""
        w_norm = entry.word.lower().strip()
        l_norm = entry.lemma.lower().strip()

        self._entries_by_word[w_norm] = entry

        if l_norm not in self._entries_by_lemma:
            self._entries_by_lemma[l_norm] = []
        self._entries_by_lemma[l_norm].append(entry)

        dialect_norm = entry.dialect.lower().strip()
        if dialect_norm not in self._entries_by_dialect:
            self._entries_by_dialect[dialect_norm] = []
        self._entries_by_dialect[dialect_norm].append(entry)

        self._trie.insert(w_norm, entry.id)
        if l_norm != w_norm:
            self._trie.insert(l_norm, entry.id)

    def exists(self, word: str) -> bool:
        """Check if a word (or lemma) exists in the lexicon."""
        if not word:
            return False
        w = word.lower().strip()
        return w in self._entries_by_word or w in self._entries_by_lemma

    def lookup(self, word: str) -> Optional[LexiconEntry]:
        """Look up a word and return its LexiconEntry if found, else None."""
        if not word:
            return None
        w = word.lower().strip()
        if w in self._entries_by_word:
            return self._entries_by_word[w]
        if w in self._entries_by_lemma and self._entries_by_lemma[w]:
            return self._entries_by_lemma[w][0]
        return None

    def get_lemma(self, word: str) -> Optional[str]:
        """Get the base lemma for a word, or None if word not in lexicon."""
        entry = self.lookup(word)
        return entry.lemma if entry else None

    def search(self, prefix: str, limit: int = 10) -> List[LexiconEntry]:
        """Find entries starting with prefix."""
        if not prefix:
            return []
        p = prefix.lower().strip()
        matched_words = self._trie.search_by_prefix(p, limit=limit)
        results: List[LexiconEntry] = []
        seen_ids: Set[str] = set()

        for w in matched_words:
            entry = self.lookup(w)
            if entry and entry.id not in seen_ids:
                seen_ids.add(entry.id)
                results.append(entry)
                if len(results) >= limit:
                    break
        return results

    def get_dialect(self, word: str) -> Optional[str]:
        """Return the dialect tag associated with the word, or None."""
        entry = self.lookup(word)
        return entry.dialect if entry else None

    def get_entries_by_dialect(self, dialect: str) -> List[LexiconEntry]:
        """Retrieve all entries associated with a specific dialect."""
        return list(self._entries_by_dialect.get(dialect.lower().strip(), []))

    def get_all_lemmas(self) -> Set[str]:
        """Return set of all unique base lemmas registered in the lexicon."""
        return set(self._entries_by_lemma.keys())

    def __len__(self) -> int:
        return len(self._entries_by_word)

    def __contains__(self, word: str) -> bool:
        return self.exists(word)
