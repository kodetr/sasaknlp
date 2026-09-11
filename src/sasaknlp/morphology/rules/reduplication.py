"""Reduplication analysis and rules for Bahasa Sasak."""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult


class ReduplicationRule(MorphologicalRule):
    """Detects and resolves full, spaced, affixed, and partial reduplication.

    Examples:
        - Full hyphenated: 'bareng-bareng' -> 'bareng'
        - Full spaced: 'bareng bareng' -> 'bareng'
        - Reduplication + suffix: 'bareng-barengan' -> 'bareng'
        - Partial (dwipurwa): 'bebatur' -> 'batur'
    """

    def __init__(self, name: str = "reduplication", confidence: float = 0.95) -> None:
        super().__init__(name=name, confidence=confidence)

    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Analyze word for reduplication patterns and return candidate roots."""
        results: List[RuleMatchResult] = []
        w = word.lower().strip()

        # 1. Full reduplication with hyphen: kata-kata
        if "-" in w:
            parts = w.split("-")
            if len(parts) == 2:
                left, right = parts[0], parts[1]
                # Exact match
                if left == right and len(left) >= min_root_length:
                    results.append(
                        RuleMatchResult(
                            rule_name="full_reduplication_hyphen",
                            root_candidate=left,
                            confidence=0.98,
                            details={"reduplication_type": "full_hyphen"},
                        )
                    )
                # Right part has suffix: e.g. bareng-barengan -> bareng
                elif right.startswith(left) and len(left) >= min_root_length:
                    suffix = right[len(left) :]
                    results.append(
                        RuleMatchResult(
                            rule_name="reduplication_suffix",
                            root_candidate=left,
                            suffix=suffix,
                            confidence=0.92,
                            details={"reduplication_type": "full_with_suffix"},
                        )
                    )

        # 2. Full reduplication with space: kata kata
        elif " " in w:
            parts = w.split(" ")
            if len(parts) == 2 and parts[0] == parts[1] and len(parts[0]) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name="full_reduplication_space",
                        root_candidate=parts[0],
                        confidence=0.95,
                        details={"reduplication_type": "full_space"},
                    )
                )

        # 3. Partial reduplication (dwipurwa): initial consonant + 'e' + consonant + ...
        # e.g., bebatur -> batur, tetulung -> tulung, sesolah -> solah
        match = re.match(r"^([bcdfghjklmnprstwyz])e(\1.*)", w)
        if match:
            first_c = match.group(1)
            rest = match.group(2)
            if len(rest) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name="partial_reduplication_dwipurwa",
                        root_candidate=rest,
                        prefix=first_c + "e",
                        confidence=0.75,
                        details={"reduplication_type": "dwipurwa"},
                    )
                )

        return results
