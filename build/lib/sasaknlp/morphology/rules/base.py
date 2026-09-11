"""Base classes and schemas for morphological rules in SasakNLP."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from sasaknlp.core.types import MorphologicalCandidate


@dataclass
class RuleMatchResult:
    """Represents the intermediate match of a morphological rule on a surface form."""
    rule_name: str
    root_candidate: str
    prefix: Optional[str] = None
    infix: Optional[str] = None
    suffix: Optional[str] = None
    confidence: float = 0.8
    details: Dict[str, Any] = None


class MorphologicalRule(ABC):
    """Abstract base class for all Sasak morphological rules."""

    def __init__(self, name: str, confidence: float = 0.8) -> None:
        self.name = name
        self.confidence = confidence

    @abstractmethod
    def apply(self, word: str, min_root_length: int = 3) -> List[RuleMatchResult]:
        """Apply rule to word and return potential candidate roots."""
        pass
