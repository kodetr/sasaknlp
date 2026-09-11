"""Tests for SasakTokenizer and SasakSentenceTokenizer."""

import unittest
from sasaknlp.tokenizer import SasakSentenceTokenizer, SasakTokenizer


class TestSasakTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = SasakTokenizer()

    def test_word_tokenization_basic(self):
        text = "tiyang mangan nasiq bareng"
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, ["tiyang", "mangan", "nasiq", "bareng"])

    def test_reduplicated_words_preserved(self):
        text = "batur-batur pade bareng-bareng lalo"
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("batur-batur", tokens)
        self.assertIn("bareng-bareng", tokens)

    def test_glottal_apostrophe_words(self):
        text = "sa'iq manuk' tepina' beli"
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("sa'iq", tokens)
        self.assertIn("tepina'", tokens)

    def test_keep_punctuation_option(self):
        text = "mangan, tindok."
        no_punct = self.tokenizer.tokenize(text, keep_punct=False)
        self.assertEqual(no_punct, ["mangan", "tindok"])

        with_punct = self.tokenizer.tokenize(text, keep_punct=True)
        self.assertEqual(with_punct, ["mangan", ",", "tindok", "."])

    def test_span_tokenization(self):
        text = "tiyang mangan"
        spans = self.tokenizer.span_tokenize(text)
        self.assertEqual(len(spans), 2)
        self.assertEqual(spans[0], ("tiyang", 0, 6))
        self.assertEqual(spans[1], ("mangan", 7, 13))


class TestSasakSentenceTokenizer(unittest.TestCase):
    def setUp(self):
        self.sent_tokenizer = SasakSentenceTokenizer()

    def test_basic_sentences(self):
        text = "Tiyang mangan. Side kaken? Wah beso!"
        sentences = self.sent_tokenizer.tokenize(text)
        self.assertEqual(len(sentences), 3)
        self.assertEqual(sentences[0], "Tiyang mangan.")
        self.assertEqual(sentences[1], "Side kaken?")
        self.assertEqual(sentences[2], "Wah beso!")

    def test_honorific_abbreviations_protection(self):
        # Tgh. (Tuan Guru Haji) and L. (Lalu) should not cause false sentence splits
        text = "Tgh. Lalu mangan nasiq. Side wah kaken."
        sentences = self.sent_tokenizer.tokenize(text)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(sentences[0], "Tgh. Lalu mangan nasiq.")
        self.assertEqual(sentences[1], "Side wah kaken.")


if __name__ == "__main__":
    unittest.main()
