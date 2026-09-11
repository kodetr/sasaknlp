"""Suffix rules and enclitic stripping for Bahasa Sasak."""

from __future__ import annotations

from typing import List

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult


class SuffixRule(MorphologicalRule):
    """Handles suffix and pronominal enclitic stripping in Bahasa Sasak."""

    def __init__(
        self,
        name: str,
        suffix: str,
        confidence: float = 0.90,
        meaning: str = "",
    ) -> None:
        super().__init__(name=name, confidence=confidence)
        self.suffix = suffix
        self.meaning = meaning

    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Strip suffix if present and remainder satisfies minimum length."""
        results: List[RuleMatchResult] = []
        w = word.lower()

        if w.endswith(self.suffix):
            remainder = w[: -len(self.suffix)]
            if len(remainder) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name=self.name,
                        root_candidate=remainder,
                        suffix=self.suffix,
                        confidence=self.confidence,
                    )
                )
                # Sasak epenthetic nasal ligature: vowel + n + de/te (e.g. kote -> kotende, bale -> balende)
                if self.suffix in ["de", "te"] and remainder.endswith("n") and len(remainder) - 1 >= min_root_length:
                    results.append(
                        RuleMatchResult(
                            rule_name=f"{self.name}_ligature_n",
                            root_candidate=remainder[:-1],
                            suffix=self.suffix,
                            confidence=self.confidence,
                        )
                    )

        return results
