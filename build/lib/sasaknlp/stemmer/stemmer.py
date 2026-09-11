"""Dictionary-Enhanced Rule-Based Stemmer for Bahasa Sasak."""

from __future__ import annotations

from typing import List, Optional, Tuple

from sasaknlp.core.config import NormalizerConfig, RankingWeights
from sasaknlp.core.types import MorphologicalCandidate, ValidationStatus
from sasaknlp.lexicon.manager import SasakLexManager
from sasaknlp.morphology.candidate_generator import CandidateGenerator
from sasaknlp.normalization.normalizer import SasakNormalizer
from sasaknlp.stemmer.ranking import CandidateRanker
from sasaknlp.stemmer.validator import DictionaryValidator


class SasakStemmer:
    """Dictionary-Enhanced Rule-Based Stemmer for Bahasa Sasak.

    Executes the multi-stage stemming pipeline:
    1. Normalization
    2. Direct Lexicon Lookup (returns immediately if word is already a known root)
    3. Morphological Rule Application & Candidate Generation
    4. Lexicon Validation
    5. Multi-Criteria Candidate Ranking
    6. Best Lemma Selection with OOV Fallback
    """

    def __init__(
        self,
        lexicon_manager: Optional[SasakLexManager] = None,
        candidate_generator: Optional[CandidateGenerator] = None,
        validator: Optional[DictionaryValidator] = None,
        ranker: Optional[CandidateRanker] = None,
        normalizer: Optional[SasakNormalizer] = None,
        dialect: str = "general",
        min_root_length: int = 3,
        enable_oov_fallback: bool = True,
    ) -> None:
        self.lexicon = lexicon_manager or SasakLexManager()
        self.normalizer = normalizer or SasakNormalizer()
        self.generator = candidate_generator or CandidateGenerator(min_root_length=min_root_length)
        self.validator = validator or DictionaryValidator(lexicon_manager=self.lexicon)
        self.ranker = ranker or CandidateRanker()
        self.dialect = dialect
        self.min_root_length = min_root_length
        self.enable_oov_fallback = enable_oov_fallback

    def stem(self, word: str) -> str:
        """Stem a single word to its base lemma."""
        lemma, _ = self.stem_with_candidate(word)
        return lemma

    def stem_with_candidate(self, word: str) -> Tuple[str, MorphologicalCandidate]:
        """Stem a word and return both the lemma string and full candidate details."""
        if not word:
            empty_cand = MorphologicalCandidate(
                word="",
                lemma_candidate="",
                rule_applied="empty",
                score=0.0,
                validation_status=ValidationStatus.INVALID,
            )
            return "", empty_cand

        # Stage 1: Text Normalization
        norm_word = self.normalizer.normalize_word(word)
        if not norm_word:
            empty_cand = MorphologicalCandidate(
                word=word,
                lemma_candidate="",
                rule_applied="empty",
                score=0.0,
                validation_status=ValidationStatus.INVALID,
            )
            return "", empty_cand

        # Stage 2: Direct Lexicon Lookup
        # If the word is already a recognized lemma in SasakLex, return immediately
        entry = self.lexicon.lookup(norm_word)
        if entry is not None and entry.lemma.lower() == norm_word:
            direct_cand = MorphologicalCandidate(
                word=word,
                lemma_candidate=entry.lemma,
                rule_applied="direct_lexicon_lookup",
                score=1.0,
                validation_status=ValidationStatus.EXACT_MATCH,
                metadata={
                    "lexicon_id": entry.id,
                    "pos": entry.pos,
                    "dialect": entry.dialect,
                    "meaning_id": entry.meaning_id,
                },
            )
            return entry.lemma, direct_cand

        # Stage 3: Candidate Generation via Morphological Rules
        candidates = self.generator.generate(norm_word)

        # Stage 4: Dictionary Validation
        validated_candidates = self.validator.validate_all(candidates)

        # Stage 5: Candidate Ranking
        ranked_candidates = self.ranker.rank_all(
            validated_candidates, target_dialect=self.dialect
        )

        if not ranked_candidates:
            fallback_cand = MorphologicalCandidate(
                word=word,
                lemma_candidate=norm_word,
                rule_applied="fallback_raw",
                score=0.1,
                validation_status=ValidationStatus.OOV,
            )
            return norm_word, fallback_cand

        best_cand = ranked_candidates[0]

        # Stage 6: Decision and OOV handling
        # If top candidate is validated in lexicon, use it
        if best_cand.validation_status == ValidationStatus.EXACT_MATCH:
            return best_cand.lemma_candidate, best_cand

        # If partial match or OOV with high confidence rule, check fallback
        if self.enable_oov_fallback:
            # If best candidate stripped affixes with confidence > 0.8, keep stripped root
            if best_cand.rule_applied != "identity" and len(best_cand.lemma_candidate) >= self.min_root_length:
                return best_cand.lemma_candidate, best_cand

        # Otherwise fallback to identity or top candidate
        return best_cand.lemma_candidate, best_cand

    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Stem a list of token strings."""
        return [self.stem(t) for t in tokens]
