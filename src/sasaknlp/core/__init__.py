"""Core package for SasakNLP containing data models, configuration, and pipeline base."""

from sasaknlp.core.config import NormalizerConfig, PipelineConfig, RankingWeights
from sasaknlp.core.pipeline import SasakNLP
from sasaknlp.core.types import (
    ErrorCategory,
    LexiconEntry,
    MorphologicalAnalysis,
    MorphologicalCandidate,
    PipelineResult,
    ValidationStatus,
)

__all__ = [
    "SasakNLP",
    "NormalizerConfig",
    "PipelineConfig",
    "RankingWeights",
    "ErrorCategory",
    "LexiconEntry",
    "MorphologicalAnalysis",
    "MorphologicalCandidate",
    "PipelineResult",
    "ValidationStatus",
]
