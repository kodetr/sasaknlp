"""Infix rules for Bahasa Sasak."""

from __future__ import annotations

import re
from typing import List

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult


class InfixRule(MorphologicalRule):
    """Detects and extracts infixes inserted after the initial root consonant.

    Example:
        tinulung -> infix 'in' -> root 'tulung'
        tumulung -> infix 'um' -> root 'tulung'
    """

    def __init__(
        self,
        name: str,
        infix: str,
        confidence: float = 0.80,
        meaning: str = "",
    ) -> None:
        super().__init__(name=name, confidence=confidence)
        self.infix = infix
        self.meaning = meaning
        # Pattern: Starts with consonant, then infix, then vowel and rest
        # e.g., ^([bcdfghjklmnpqrstvwxyz])in([aeiou].*)
        self.pattern = re.compile(
            rf"^([bcdfghjklmnpqrstvwxyz]){re.escape(infix)}([aeiou].*)", re.IGNORECASE
        )

    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Apply infix extraction rule."""
        results: List[RuleMatchResult] = []
        w = word.lower()

        match = self.pattern.match(w)
        if match:
            first_cons = match.group(1)
            vowel_rest = match.group(2)
            root_cand = first_cons + vowel_rest
            if len(root_cand) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name=self.name,
                        root_candidate=root_cand,
                        infix=self.infix,
                        confidence=self.confidence,
                    )
                )

        return results
