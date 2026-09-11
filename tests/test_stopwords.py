"""Unit tests for the Sasak stopwords module."""

import unittest

from sasaknlp import SasakNLP, SasakStopwords, get_stopwords, is_stopword, remove_stopwords


class TestSasakStopwords(unittest.TestCase):
    """Test suite for SasakStopwords class and functional helpers."""

    def test_default_stopwords_loading(self):
        """Test default loading of Sasak stopwords."""
        stops = get_stopwords()
        self.assertIsInstance(stops, set)
        self.assertGreater(len(stops), 100)

        # Verify essential core function words
        core_expected = [
            "saq",
            "dait",
            "leq",
            "leman",
            "ojok",
            "siq",
            "ndeq",
            "pade",
            "tiang",
            "side",
            "nike",
            "niki",
            "laguq",
            "sengaq",
            "lamun",
            "terus",
        ]
        for word in core_expected:
            self.assertIn(word, stops, f"Expected '{word}' to be in default stopwords")

    def test_is_stopword(self):
        """Test is_stopword boolean check with case and whitespace insensitivity."""
        self.assertTrue(is_stopword("dait"))
        self.assertTrue(is_stopword("DAIT"))
        self.assertTrue(is_stopword(" leq "))
        self.assertTrue(is_stopword("Ndeq"))

        # Content words should not be stopwords
        self.assertFalse(is_stopword("mangan"))
        self.assertFalse(is_stopword("tindok"))
        self.assertFalse(is_stopword("bale"))
        self.assertFalse(is_stopword(""))

    def test_remove_stopwords_tokens(self):
        """Test filtering tokens from a list."""
        tokens = ["tiang", "mangan", "nasiq", "leq", "bale", "dait", "nginem"]
        filtered = remove_stopwords(tokens)
        self.assertEqual(filtered, ["mangan", "nasiq", "bale", "nginem"])

    def test_remove_stopwords_text(self):
        """Test filtering stopwords from a raw text string."""
        text = "tiang mangan nasiq leq bale dait nginem kupi"
        filtered = remove_stopwords(text)
        expected = "mangan nasiq bale nginem kupi"
        self.assertEqual(filtered, expected)

    def test_dialect_specific_stopwords(self):
        """Test dialect markers inclusion and separation."""
        sw = SasakStopwords()

        # Core without dialect markers
        core_only = sw.get_stopwords(include_dialect=False)
        self.assertIn("dait", core_only)
        self.assertNotIn("menu", core_only)
        self.assertNotIn("ngeno", core_only)

        # Selaparang dialect
        selaparang_stops = sw.get_stopwords(dialect="selaparang")
        self.assertIn("menu", selaparang_stops)
        self.assertIn("meni", selaparang_stops)

        # Ngeno-ngene dialect
        ngeno_stops = sw.get_stopwords(dialect="ngeno_ngene")
        self.assertIn("ngeno", ngeno_stops)
        self.assertIn("ngene", ngeno_stops)

    def test_custom_stopwords_add_remove(self):
        """Test adding and removing custom stopwords."""
        sw = SasakStopwords()
        self.assertFalse(sw.is_stopword("kadusol"))

        sw.add("kadusol")
        self.assertTrue(sw.is_stopword("kadusol"))

        sw.remove("kadusol")
        self.assertFalse(sw.is_stopword("kadusol"))

    def test_pipeline_integration(self):
        """Test integration with SasakNLP pipeline class."""
        nlp = SasakNLP()
        self.assertIsNotNone(nlp.stopwords)

        tokens = ["tiang", "turu", "leq", "gedeng"]
        filtered_tokens = nlp.remove_stopwords(tokens)
        self.assertEqual(filtered_tokens, ["turu", "gedeng"])

        text = "side lumbar ojok peken"
        filtered_text = nlp.remove_stopwords(text)
        self.assertEqual(filtered_text, "lumbar peken")


if __name__ == "__main__":
    unittest.main()
