"""Tests for DialectManager and DialectDetector."""

import unittest
from sasaknlp.dialect import DialectDetector, DialectManager


class TestDialectModule(unittest.TestCase):
    def setUp(self):
        self.manager = DialectManager()
        self.detector = DialectDetector(self.manager)

    def test_supported_dialects(self):
        dialects = self.manager.get_supported_dialects()
        self.assertIn("general", dialects)
        self.assertIn("selaparang", dialects)
        self.assertIn("ngeno_ngene", dialects)

    def test_detector_selaparang_markers(self):
        tokens = ["tiyang", "mangan", "menu", "kaken"]
        dialect, conf = self.detector.detect(tokens)
        self.assertEqual(dialect, "selaparang")
        self.assertGreater(conf, 0.6)

    def test_detector_fallback_general(self):
        tokens = ["batur", "anak", "lalo"]
        dialect, conf = self.detector.detect(tokens)
        self.assertEqual(dialect, "general")
        self.assertEqual(conf, 0.5)

    def test_empty_tokens(self):
        dialect, conf = self.detector.detect([])
        self.assertEqual(dialect, "general")
        self.assertEqual(conf, 0.0)


if __name__ == "__main__":
    unittest.main()
