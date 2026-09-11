"""Combination and circumfix rules for Bahasa Sasak."""

from __future__ import annotations

from typing import List

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult


class CombinationRule(MorphologicalRule):
    """Handles circumfixes and simultaneous multi-affix combinations.

    Example:
        pe-...-an : pemangan -> mangan (with pe-)
        te-...-ang : tetulungang -> tulung
        ka-...-an : kasolahan -> solah
    """

    def __init__(
        self,
        name: str,
        prefix: str,
        suffix: str,
        confidence: float = 0.90,
        meaning: str = "",
    ) -> None:
        super().__init__(name=name, confidence=confidence)
        self.prefix = prefix
        self.suffix = suffix
        self.meaning = meaning

    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Strip both prefix and suffix simultaneously if both are present."""
        results: List[RuleMatchResult] = []
        w = word.lower()

        if w.startswith(self.prefix) and w.endswith(self.suffix):
            core = w[len(self.prefix) : -len(self.suffix)]
            if len(core) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name=self.name,
                        root_candidate=core,
                        prefix=self.prefix,
                        suffix=self.suffix,
                        confidence=self.confidence,
                    )
                )

        return results
