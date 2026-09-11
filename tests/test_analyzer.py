"""Tests for MorphologicalAnalyzer."""

import unittest
from sasaknlp.morphology import MorphologicalAnalyzer


class TestMorphologicalAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MorphologicalAnalyzer()

    def test_structured_analysis_prefix(self):
        res = self.analyzer.analyze("tepinaq")
        self.assertEqual(res.surface_form, "tepinaq")
        self.assertEqual(res.lemma, "pinaq")
        self.assertEqual(res.prefix, "te")
        self.assertIsNone(res.suffix)
        self.assertEqual(res.rule_applied, "passive_te")
        self.assertGreater(res.confidence, 0.8)
        self.assertFalse(res.is_oov)

    def test_structured_analysis_suffix(self):
        res = self.analyzer.analyze("tulungang")
        self.assertEqual(res.lemma, "tulung")
        self.assertEqual(res.suffix, "ang")
        self.assertIsNone(res.prefix)

    def test_structured_analysis_reduplication(self):
        res = self.analyzer.analyze("bareng-bareng")
        self.assertEqual(res.lemma, "bareng")
        self.assertIsNotNone(res.reduplication)

    def test_to_dict(self):
        res = self.analyzer.analyze("mangan")
        d = res.to_dict()
        self.assertEqual(d["lemma"], "mangan")
        self.assertEqual(d["surface_form"], "mangan")


if __name__ == "__main__":
    unittest.main()
