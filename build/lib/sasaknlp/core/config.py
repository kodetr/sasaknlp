"""Configuration dataclasses for SasakNLP pipeline and submodules.

Enables flexible parameter tuning for candidate ranking, normalizer settings,
dialect handling, and path resolutions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RankingWeights:
    """Configurable weights for the CandidateRanker scoring formula.

    Score = w_lex * S_lex + w_morph * S_morph + w_conf * S_conf + w_freq * S_freq + w_dial * S_dial
    """
    lexicon_match: float = 0.40
    morphological_validity: float = 0.25
    rule_confidence: float = 0.15
    frequency: float = 0.10
    dialect_compatibility: float = 0.10

    def validate(self) -> None:
        """Ensure all weights are non-negative."""
        weights = [
            self.lexicon_match,
            self.morphological_validity,
            self.rule_confidence,
            self.frequency,
            self.dialect_compatibility,
        ]
        if any(w < 0.0 for w in weights):
            raise ValueError(f"All ranking weights must be non-negative. Got: {self}")


@dataclass
class NormalizerConfig:
    """Settings controlling text normalization behavior."""
    lowercase: bool = True
    unicode_form: str = "NFC"
    remove_extra_whitespace: bool = True
    normalize_quotes: bool = True
    preserve_hyphenated_words: bool = True
    strip_punctuation: bool = False


@dataclass
class PipelineConfig:
    """Comprehensive configuration for the SasakNLP pipeline."""
    dialect: str = "auto"
    custom_lexicon_path: Optional[Path] = None
    custom_rules_path: Optional[Path] = None
    normalizer: NormalizerConfig = field(default_factory=NormalizerConfig)
    ranking_weights: RankingWeights = field(default_factory=RankingWeights)
    min_root_length: int = 3
    handle_reduplication: bool = True
    enable_oov_fallback: bool = True
