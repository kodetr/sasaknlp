"""Tests for DictionaryValidator and CandidateRanker."""

import unittest
from sasaknlp.core.config import RankingWeights
from sasaknlp.core.types import MorphologicalCandidate, ValidationStatus
from sasaknlp.lexicon import SasakLexManager
from sasaknlp.stemmer import CandidateRanker, DictionaryValidator


class TestValidatorAndRanker(unittest.TestCase):
    def setUp(self):
        self.lexicon = SasakLexManager()
        self.validator = DictionaryValidator(lexicon_manager=self.lexicon)
        self.ranker = CandidateRanker()

    def test_validation_exact_match(self):
        cand = MorphologicalCandidate(
            word="mangan",
            lemma_candidate="mangan",
            rule_applied="identity",
            score=0.5,
        )
        val = self.validator.validate(cand)
        self.assertEqual(val.validation_status, ValidationStatus.EXACT_MATCH)
        self.assertIn("pos", val.metadata)

    def test_validation_oov(self):
        cand = MorphologicalCandidate(
            word="unknownxyz",
            lemma_candidate="unknownxyz",
            rule_applied="identity",
            score=0.5,
        )
        val = self.validator.validate(cand)
        self.assertEqual(val.validation_status, ValidationStatus.OOV)

    def test_validation_invalid_phonotactics(self):
        cand = MorphologicalCandidate(
            word="zzz",
            lemma_candidate="zzz",  # No vowels
            rule_applied="test",
            score=0.5,
        )
        val = self.validator.validate(cand)
        self.assertEqual(val.validation_status, ValidationStatus.INVALID)

    def test_candidate_ranking_prioritizes_exact_match(self):
        c1 = MorphologicalCandidate(
            word="tepinaq",
            lemma_candidate="pinaq",
            removed_prefix="te",
            rule_applied="passive_te",
            score=0.9,
            validation_status=ValidationStatus.EXACT_MATCH,
        )
        c2 = MorphologicalCandidate(
            word="tepinaq",
            lemma_candidate="tepinaq",
            rule_applied="identity",
            score=0.5,
            validation_status=ValidationStatus.OOV,
        )
        ranked = self.ranker.rank_all([c2, c1])
        self.assertEqual(ranked[0].lemma_candidate, "pinaq")
        self.assertGreater(ranked[0].score, ranked[1].score)

    def test_ranking_weights_custom(self):
        w = RankingWeights(lexicon_match=0.5, morphological_validity=0.5)
        r = CandidateRanker(weights=w)
        self.assertEqual(r.weights.lexicon_match, 0.5)


if __name__ == "__main__":
    unittest.main()
