"""SasakNLP: Research-Grade Natural Language Processing Toolkit for Bahasa Sasak.

An open-source NLP and morphological processing toolkit for the low-resource
Sasak language of Lombok, Indonesia.
"""

__version__ = "0.1.0"
__author__ = "SasakNLP Contributors"

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
from sasaknlp.dialect import DialectDetector, DialectManager
from sasaknlp.lexicon import LexiconLoader, PrefixTrie, SasakLexManager
from sasaknlp.morphology import CandidateGenerator, MorphologicalAnalyzer
from sasaknlp.normalization import SasakNormalizer
from sasaknlp.stemmer import CandidateRanker, DictionaryValidator, SasakStemmer
from sasaknlp.tokenizer import SasakSentenceTokenizer, SasakTokenizer


def get_version() -> str:
    """Return package version string."""
    return __version__


__all__ = [
    "__version__",
    "get_version",
    "SasakNLP",
    "SasakStemmer",
    "MorphologicalAnalyzer",
    "CandidateGenerator",
    "SasakLexManager",
    "LexiconLoader",
    "PrefixTrie",
    "SasakNormalizer",
    "SasakTokenizer",
    "SasakSentenceTokenizer",
    "DictionaryValidator",
    "CandidateRanker",
    "DialectManager",
    "DialectDetector",
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
