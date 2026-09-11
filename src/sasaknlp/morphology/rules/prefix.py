"""Prefix rules and morphophonemic alternation handling for Bahasa Sasak."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult


class PrefixRule(MorphologicalRule):
    """Handles prefix stripping and nasal morphophonemic transformations."""

    def __init__(
        self,
        name: str,
        prefix: str,
        confidence: float = 0.85,
        phonological_rules: Optional[List[Dict[str, Any]]] = None,
        meaning: str = "",
    ) -> None:
        super().__init__(name=name, confidence=confidence)
        self.prefix = prefix
        self.meaning = meaning
        self.phonological_rules = phonological_rules or []

    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Strip prefix or restore underlying root through phonological mapping."""
        results: List[RuleMatchResult] = []
        w = word.lower()

        # Check phonological rules first if present (nasal mutations)
        if self.phonological_rules:
            for rule in self.phonological_rules:
                pattern = rule.get("pattern", "")
                restores = rule.get("restores", [])
                match = re.match(pattern, w)
                if match:
                    for template in restores:
                        candidate = re.sub(pattern, template, w)
                        if len(candidate) >= min_root_length and candidate != w:
                            results.append(
                                RuleMatchResult(
                                    rule_name=self.name,
                                    root_candidate=candidate,
                                    prefix=self.prefix,
                                    confidence=self.confidence,
                                    details={"phonological_restore": template},
                                )
                            )
            if results:
                return results

        # Direct prefix stripping
        if w.startswith(self.prefix):
            remainder = w[len(self.prefix) :]
            if len(remainder) >= min_root_length:
                results.append(
                    RuleMatchResult(
                        rule_name=self.name,
                        root_candidate=remainder,
                        prefix=self.prefix,
                        confidence=self.confidence,
                    )
                )

        return results
