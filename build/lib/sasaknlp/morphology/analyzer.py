"""Morphological analyzer producing structured morphological descriptions."""

from __future__ import annotations

from typing import List, Optional

from sasaknlp.core.types import MorphologicalAnalysis, ValidationStatus
from sasaknlp.stemmer.stemmer import SasakStemmer


class MorphologicalAnalyzer:
    """Performs detailed morphological breakdown of words in Bahasa Sasak.

    Produces structured MorphologicalAnalysis records containing identified
    prefixes, infixes, suffixes, reduplication status, confidence, and dialect.
    """

    def __init__(self, stemmer: Optional[SasakStemmer] = None, dialect: str = "general") -> None:
        self.stemmer = stemmer or SasakStemmer(dialect=dialect)
        self.dialect = dialect

    def analyze(self, word: str) -> MorphologicalAnalysis:
        """Analyze a single word token and return structured morphological decomposition.

        Args:
            word: Surface form to be analyzed.

        Returns:
            MorphologicalAnalysis instance.
        """
        if not word or not word.strip():
            return MorphologicalAnalysis(
                surface_form=word,
                lemma=word,
                dialect=self.dialect,
                confidence=0.0,
                is_oov=True,
            )

        lemma, best_cand = self.stemmer.stem_with_candidate(word)

        # Detect reduplication details
        redup_type = best_cand.metadata.get("reduplication_type")
        if not redup_type and "-" in word:
            redup_type = "hyphenated"

        is_oov = best_cand.validation_status in (ValidationStatus.OOV, ValidationStatus.INVALID)
        token_dialect = best_cand.metadata.get("dialect", self.dialect)

        # Calibrated confidence: if exact match in lexicon, high confidence; else candidate score
        if best_cand.validation_status == ValidationStatus.EXACT_MATCH:
            confidence = max(0.90, best_cand.score)
        elif best_cand.validation_status == ValidationStatus.PARTIAL_MATCH:
            confidence = min(0.85, best_cand.score)
        else:
            confidence = min(0.70, best_cand.score)

        return MorphologicalAnalysis(
            surface_form=word,
            lemma=lemma,
            prefix=best_cand.removed_prefix,
            infix=best_cand.removed_infix,
            suffix=best_cand.removed_suffix,
            rule_applied=best_cand.rule_applied,
            dialect=token_dialect,
            confidence=round(confidence, 4),
            reduplication=redup_type,
            is_oov=is_oov,
            metadata=best_cand.metadata,
        )

    def analyze_tokens(self, tokens: List[str]) -> List[MorphologicalAnalysis]:
        """Analyze an ordered list of word tokens."""
        return [self.analyze(t) for t in tokens]
