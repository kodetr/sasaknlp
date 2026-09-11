"""Morphology package for SasakNLP."""

from sasaknlp.morphology.analyzer import MorphologicalAnalyzer
from sasaknlp.morphology.candidate_generator import CandidateGenerator
from sasaknlp.morphology.rules import (
    CombinationRule,
    InfixRule,
    MorphologicalRule,
    PrefixRule,
    ReduplicationRule,
    RuleMatchResult,
    SuffixRule,
    load_rules_from_config,
)

__all__ = [
    "MorphologicalAnalyzer",
    "CandidateGenerator",
    "MorphologicalRule",
    "RuleMatchResult",
    "PrefixRule",
    "SuffixRule",
    "InfixRule",
    "CombinationRule",
    "ReduplicationRule",
    "load_rules_from_config",
]
