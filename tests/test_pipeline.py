"""Tests for end-to-end SasakNLP pipeline."""

import unittest
from sasaknlp import SasakNLP


class TestSasakNLPPipeline(unittest.TestCase):
    def setUp(self):
        self.nlp = SasakNLP()

    def test_process_full_pipeline(self):
        text = "Tiyang mangan nasiq bareng-bareng!"
        result = self.nlp.process(text)

        self.assertEqual(result.text, text)
        self.assertIn("mangan", result.tokens)
        self.assertIn("bareng-bareng", result.tokens)
        self.assertEqual(len(result.tokens), len(result.analyses))
        self.assertEqual(len(result.tokens), len(result.lemmas))
        self.assertEqual(result.dialect, "selaparang")

        d = result.to_dict()
        self.assertIn("tokens", d)
        self.assertIn("lemmas", d)
        self.assertIn("analyses", d)

    def test_convenience_stem_word_and_sentence(self):
        # Single word
        self.assertEqual(self.nlp.stem("tepinaq"), "pinaq")
        # Full sentence
        lemmas = self.nlp.stem("tiyang mangan")
        self.assertEqual(lemmas, ["tiyang", "mangan"])

    def test_convenience_analyze(self):
        analysis = self.nlp.analyze("tulungang")
        self.assertEqual(analysis.lemma, "tulung")

    def test_empty_text(self):
        result = self.nlp.process("")
        self.assertEqual(len(result.tokens), 0)
        self.assertEqual(len(result.lemmas), 0)


if __name__ == "__main__":
    unittest.main()
