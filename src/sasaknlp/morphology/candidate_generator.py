"""Morphological candidate generator for Bahasa Sasak."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Set, Union

from sasaknlp.core.types import MorphologicalCandidate, ValidationStatus
from sasaknlp.morphology.rules import (
    MorphologicalRule,
    load_rules_from_config,
)


class CandidateGenerator:
    """Generates root candidates from an inflected word using morphological rules.

    Given a word, systematically tests prefix, suffix, infix, circumfix, and
    reduplication rules to generate an exhaustive list of candidate root forms.
    """

    def __init__(
        self,
        rules: Optional[List[MorphologicalRule]] = None,
        config_path: Optional[Union[str, Path]] = None,
        min_root_length: int = 3,
    ) -> None:
        self.rules = rules if rules is not None else load_rules_from_config(config_path)
        self.min_root_length = min_root_length

    def generate(self, word: str) -> List[MorphologicalCandidate]:
        """Generate all plausible root candidates for the input word.

        Args:
            word: Surface form to be analyzed.

        Returns:
            List of MorphologicalCandidate instances with rule provenance and initial confidence.
        """
        if not word:
            return []

        clean_word = word.lower().strip()
        candidates: List[MorphologicalCandidate] = []
        seen_keys: Set[str] = set()

        def _add_candidate(cand: MorphologicalCandidate) -> None:
            key = f"{cand.lemma_candidate}|{cand.removed_prefix}|{cand.removed_infix}|{cand.removed_suffix}|{cand.rule_applied}"
            if key not in seen_keys and len(cand.lemma_candidate) >= self.min_root_length:
                seen_keys.add(key)
                candidates.append(cand)

        # 1. Identity candidate (the word itself might be a valid root)
        _add_candidate(
            MorphologicalCandidate(
                word=word,
                lemma_candidate=clean_word,
                removed_prefix=None,
                removed_infix=None,
                removed_suffix=None,
                rule_applied="identity",
                score=0.5,
                validation_status=ValidationStatus.UNVALIDATED,
            )
        )

        # 2. Apply all loaded rules (Prefixes, Suffixes, Infixes, Combinations, Reduplication)
        for rule in self.rules:
            matches = rule.apply(clean_word, min_root_length=self.min_root_length)
            for m in matches:
                cand = MorphologicalCandidate(
                    word=word,
                    lemma_candidate=m.root_candidate,
                    removed_prefix=m.prefix,
                    removed_infix=m.infix,
                    removed_suffix=m.suffix,
                    rule_applied=m.rule_name,
                    score=m.confidence,
                    validation_status=ValidationStatus.UNVALIDATED,
                    metadata=m.details or {},
                )
                _add_candidate(cand)

                # 3. Two-step composition: If a prefix was removed, test suffix rules on remainder
                if m.prefix and not m.suffix and not m.infix:
                    for sub_rule in self.rules:
                        sub_matches = sub_rule.apply(m.root_candidate, min_root_length=self.min_root_length)
                        for sm in sub_matches:
                            if sm.suffix and not sm.prefix:
                                comp_cand = MorphologicalCandidate(
                                    word=word,
                                    lemma_candidate=sm.root_candidate,
                                    removed_prefix=m.prefix,
                                    removed_infix=None,
                                    removed_suffix=sm.suffix,
                                    rule_applied=f"{m.rule_name}+{sm.rule_name}",
                                    score=min(m.confidence, sm.confidence) * 0.95,
                                    validation_status=ValidationStatus.UNVALIDATED,
                                )
                                _add_candidate(comp_cand)

                # 4. Sastrawi-style composition: If a clitic or suffix was removed, test rules on remainder
                if m.suffix and not m.prefix and not m.infix:
                    for sub_rule in self.rules:
                        sub_matches = sub_rule.apply(m.root_candidate, min_root_length=self.min_root_length)
                        for sm in sub_matches:
                            pref = sm.prefix
                            suff = f"{sm.suffix}+{m.suffix}" if sm.suffix else m.suffix
                            comp_cand = MorphologicalCandidate(
                                word=word,
                                lemma_candidate=sm.root_candidate,
                                removed_prefix=pref,
                                removed_infix=sm.infix,
                                removed_suffix=suff,
                                rule_applied=f"{m.rule_name}+{sm.rule_name}",
                                score=min(m.confidence, sm.confidence) * 0.95,
                                validation_status=ValidationStatus.UNVALIDATED,
                            )
                            _add_candidate(comp_cand)

        return candidates
