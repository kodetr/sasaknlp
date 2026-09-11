"""Dictionary validator for morphological root candidates."""

from __future__ import annotations

from typing import List, Optional

from sasaknlp.core.types import MorphologicalCandidate, ValidationStatus
from sasaknlp.lexicon.manager import SasakLexManager


class DictionaryValidator:
    """Validates candidate root forms against the SasakLex dictionary.

    Assigns validation statuses: EXACT_MATCH, PARTIAL_MATCH, OOV, or INVALID.
    """

    def __init__(self, lexicon_manager: Optional[SasakLexManager] = None) -> None:
        self.lexicon = lexicon_manager or SasakLexManager()

    def validate(self, candidate: MorphologicalCandidate) -> MorphologicalCandidate:
        """Validate a single morphological candidate against the lexicon.

        Updates candidate.validation_status and populates candidate.metadata
        with lexical information (pos, dialect, frequency, meaning_id).
        """
        cand_root = candidate.lemma_candidate.lower().strip()

        # Phonotactic check: must have at least one vowel
        has_vowel = any(c in "aeiouéè" for c in cand_root)
        if not has_vowel or len(cand_root) < 2:
            candidate.validation_status = ValidationStatus.INVALID
            return candidate

        # 1. Exact match check
        entry = self.lexicon.lookup(cand_root)
        if entry is not None:
            candidate.validation_status = ValidationStatus.EXACT_MATCH
            candidate.metadata["lexicon_id"] = entry.id
            candidate.metadata["pos"] = entry.pos
            candidate.metadata["dialect"] = entry.dialect
            candidate.metadata["frequency"] = entry.frequency
            candidate.metadata["meaning_id"] = entry.meaning_id
            return candidate

        # 2. Check if lemma exists in lemma set
        if cand_root in self.lexicon.get_all_lemmas():
            candidate.validation_status = ValidationStatus.EXACT_MATCH
            return candidate

        # 3. Partial match check (e.g., prefix in lexicon)
        prefix_matches = self.lexicon.search(cand_root, limit=3)
        if prefix_matches:
            candidate.validation_status = ValidationStatus.PARTIAL_MATCH
            candidate.metadata["partial_matches"] = [p.lemma for p in prefix_matches]
            return candidate

        # 4. Out Of Vocabulary
        candidate.validation_status = ValidationStatus.OOV
        return candidate

    def validate_all(self, candidates: List[MorphologicalCandidate]) -> List[MorphologicalCandidate]:
        """Validate an entire list of candidates."""
        return [self.validate(c) for c in candidates]
