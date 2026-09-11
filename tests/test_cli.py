"""Tests for SasakNLP Command Line Interface."""

import unittest
from unittest.mock import patch
from io import StringIO

from sasaknlp.cli.main import main


class TestCLI(unittest.TestCase):
    def test_cli_stem(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            code = main(["stem", "tepinaq"])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn("Lemma: pinaq", output)

    def test_cli_analyze(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            code = main(["analyze", "tulungang"])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn("Lemma        : tulung", output)
            self.assertIn("Suffix       : ang", output)

    def test_cli_process(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            code = main(["process", "tiyang mangan"])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn("Lemmas          : ['tiyang', 'mangan']", output)

    def test_cli_lexicon_lookup(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            code = main(["lexicon", "lookup", "mangan"])
            self.assertEqual(code, 0)
            output = fake_out.getvalue()
            self.assertIn('"lemma": "mangan"', output)

    def test_cli_help(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            code = main([])
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
