"""Morphological rule registry and factory for Bahasa Sasak."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Union

from sasaknlp.morphology.rules.base import MorphologicalRule, RuleMatchResult
from sasaknlp.morphology.rules.combination import CombinationRule
from sasaknlp.morphology.rules.infix import InfixRule
from sasaknlp.morphology.rules.prefix import PrefixRule
from sasaknlp.morphology.rules.reduplication import ReduplicationRule
from sasaknlp.morphology.rules.suffix import SuffixRule

DEFAULT_RULES_CONFIG = Path(__file__).parent / "rules_config.json"


def load_rules_from_config(config_path: Optional[Union[str, Path]] = None) -> List[MorphologicalRule]:
    """Load and instantiate all morphological rules defined in JSON configuration."""
    path = Path(config_path or DEFAULT_RULES_CONFIG)
    if not path.exists():
        raise FileNotFoundError(f"Rules configuration file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rules: List[MorphologicalRule] = []

    # 1. Reduplication rule (first priority for compound/duplicated structures)
    rules.append(ReduplicationRule())

    # 2. Combinations (circumfixes)
    for c in data.get("combinations", []):
        rules.append(
            CombinationRule(
                name=c.get("name", "combination"),
                prefix=c.get("prefix", ""),
                suffix=c.get("suffix", ""),
                confidence=float(c.get("confidence", 0.90)),
                meaning=c.get("meaning", ""),
            )
        )

    # 3. Prefixes
    for p in data.get("prefixes", []):
        rules.append(
            PrefixRule(
                name=p.get("name", "prefix"),
                prefix=p.get("prefix", ""),
                confidence=float(p.get("confidence", 0.85)),
                phonological_rules=p.get("phonological_rules", []),
                meaning=p.get("meaning", ""),
            )
        )

    # 4. Suffixes
    for s in data.get("suffixes", []):
        rules.append(
            SuffixRule(
                name=s.get("name", "suffix"),
                suffix=s.get("suffix", ""),
                confidence=float(s.get("confidence", 0.90)),
                meaning=s.get("meaning", ""),
            )
        )

    # 5. Infixes
    for i in data.get("infixes", []):
        rules.append(
            InfixRule(
                name=i.get("name", "infix"),
                infix=i.get("infix", ""),
                confidence=float(i.get("confidence", 0.80)),
                meaning=i.get("meaning", ""),
            )
        )

    return rules


__all__ = [
    "MorphologicalRule",
    "RuleMatchResult",
    "PrefixRule",
    "SuffixRule",
    "InfixRule",
    "CombinationRule",
    "ReduplicationRule",
    "load_rules_from_config",
    "DEFAULT_RULES_CONFIG",
]
