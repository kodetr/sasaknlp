"""Tests for SasakStemmer."""

import unittest
from sasaknlp.stemmer import SasakStemmer


class TestSasakStemmer(unittest.TestCase):
    def setUp(self):
        self.stemmer = SasakStemmer()

    def test_direct_lexicon_lookup(self):
        self.assertEqual(self.stemmer.stem("mangan"), "mangan")
        self.assertEqual(self.stemmer.stem("tindok"), "tindok")

    def test_prefix_stemming(self):
        self.assertEqual(self.stemmer.stem("tepinaq"), "pinaq")
        self.assertEqual(self.stemmer.stem("pemangan"), "mangan")

    def test_suffix_stemming(self):
        self.assertEqual(self.stemmer.stem("tulungang"), "tulung")
        self.assertEqual(self.stemmer.stem("kelororan"), "keloror")
        self.assertEqual(self.stemmer.stem("baturne"), "batur")

    def test_reduplication_stemming(self):
        self.assertEqual(self.stemmer.stem("bareng-bareng"), "bareng")

    def test_circumfix_stemming(self):
        self.assertEqual(self.stemmer.stem("kasolahan"), "solah")

    def test_stem_tokens(self):
        tokens = ["tiyang", "tepinaq", "tulungang"]
        lemmas = self.stemmer.stem_tokens(tokens)
        self.assertEqual(lemmas, ["tiyang", "pinaq", "tulung"])

    def test_empty_string(self):
        self.assertEqual(self.stemmer.stem(""), "")


if __name__ == "__main__":
    unittest.main()
