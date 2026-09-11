"""Tests for SasakLexManager, PrefixTrie, and LexiconLoader."""

import unittest
from sasaknlp.core.types import LexiconEntry
from sasaknlp.lexicon import PrefixTrie, SasakLexManager


class TestPrefixTrie(unittest.TestCase):
    def setUp(self):
        self.trie = PrefixTrie()
        for word in ["mangan", "manuk", "mandi", "tindok"]:
            self.trie.insert(word)

    def test_contains(self):
        self.assertTrue(self.trie.contains("mangan"))
        self.assertTrue(self.trie.contains("tindok"))
        self.assertFalse(self.trie.contains("mang"))
        self.assertFalse(self.trie.contains("lalo"))

    def test_search_by_prefix(self):
        results = self.trie.search_by_prefix("ma")
        self.assertIn("mangan", results)
        self.assertIn("manuk", results)
        self.assertIn("mandi", results)
        self.assertNotIn("tindok", results)

    def test_longest_prefix(self):
        prefix, _ = self.trie.find_longest_prefix("manganang")
        self.assertEqual(prefix, "mangan")


class TestSasakLexManager(unittest.TestCase):
    def setUp(self):
        self.lexicon = SasakLexManager()

    def test_default_lexicon_loaded(self):
        self.assertGreater(len(self.lexicon), 20)

    def test_exists(self):
        self.assertTrue(self.lexicon.exists("mangan"))
        self.assertTrue(self.lexicon.exists("pinaq"))
        self.assertFalse(self.lexicon.exists("not_a_real_sasak_word_xyz"))

    def test_lookup(self):
        entry = self.lexicon.lookup("mangan")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.lemma, "mangan")
        self.assertEqual(entry.pos, "VERB")
        self.assertEqual(entry.meaning_id, "makan")

    def test_get_lemma(self):
        self.assertEqual(self.lexicon.get_lemma("mangan"), "mangan")
        self.assertIsNone(self.lexicon.get_lemma("unknown_word"))

    def test_search(self):
        results = self.lexicon.search("ti")
        words = [r.word for r in results]
        self.assertTrue(any("tiyang" in w or "tindok" in w for w in words))

    def test_get_dialect(self):
        self.assertEqual(self.lexicon.get_dialect("kaken"), "selaparang")
        self.assertEqual(self.lexicon.get_dialect("mangan"), "general")

    def test_add_entry_dynamic(self):
        entry = LexiconEntry(
            id="TEST01",
            word="uji",
            lemma="uji",
            pos="VERB",
            meaning_id="tes",
            dialect="general",
        )
        self.lexicon.add_entry(entry)
        self.assertTrue(self.lexicon.exists("uji"))
        self.assertEqual(self.lexicon.get_lemma("uji"), "uji")


if __name__ == "__main__":
    unittest.main()
