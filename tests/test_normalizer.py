"""Tests for SasakNormalizer and normalization rules."""

import unittest
from sasaknlp.normalization import SasakNormalizer
from sasaknlp.core.config import NormalizerConfig


class TestSasakNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = SasakNormalizer()

    def test_lowercase(self):
        self.assertEqual(self.normalizer.normalize("TIYANG Mangan"), "tiyang mangan")

    def test_unicode_and_quotes(self):
        # Curly quotes and modifier apostrophes
        raw = "“sa’iq” ‘tepinaq’"
        expected = '"sa\'iq" \'tepinaq\''
        self.assertEqual(self.normalizer.normalize(raw), expected)

    def test_collapse_whitespace(self):
        raw = "   mangan    nasiq \n\t bareng   "
        self.assertEqual(self.normalizer.normalize(raw), "mangan nasiq bareng")

    def test_strip_punctuation_option(self):
        cfg = NormalizerConfig(strip_punctuation=True, preserve_hyphenated_words=True)
        norm = SasakNormalizer(config=cfg)
        raw = "mangan, nasiq; bareng-bareng!"
        self.assertEqual(norm.normalize(raw), "mangan nasiq bareng-bareng")

    def test_normalize_word(self):
        self.assertEqual(self.normalizer.normalize_word('"mangan!"'), "mangan")
        self.assertEqual(self.normalizer.normalize_word("...tepinaq..."), "tepinaq")
        self.assertEqual(self.normalizer.normalize_word("sa'iq"), "sa'iq")
        self.assertEqual(self.normalizer.normalize_word(""), "")


if __name__ == "__main__":
    unittest.main()
