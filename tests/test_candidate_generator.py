"""Tests for CandidateGenerator."""

import unittest
from sasaknlp.morphology import CandidateGenerator


class TestCandidateGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CandidateGenerator()

    def test_identity_candidate_always_present(self):
        candidates = self.generator.generate("mangan")
        self.assertTrue(any(c.lemma_candidate == "mangan" and c.rule_applied == "identity" for c in candidates))

    def test_affix_candidate_generation(self):
        candidates = self.generator.generate("tepinaq")
        roots = [c.lemma_candidate for c in candidates]
        self.assertIn("pinaq", roots)
        self.assertIn("tepinaq", roots)

    def test_composite_prefix_suffix_generation(self):
        candidates = self.generator.generate("tetulungang")
        roots = [c.lemma_candidate for c in candidates]
        self.assertIn("tulung", roots)

    def test_empty_string(self):
        candidates = self.generator.generate("")
        self.assertEqual(len(candidates), 0)


if __name__ == "__main__":
    unittest.main()
