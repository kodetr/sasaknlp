"""Tests for Evaluation module (metrics, error analysis, benchmark evaluator)."""

import unittest
from sasaknlp.core.types import ErrorCategory
from sasaknlp.evaluation import BenchmarkEvaluator, ErrorAnalyzer
from sasaknlp.evaluation.metrics import compute_accuracy, compute_precision_recall_f1


class TestEvaluationModule(unittest.TestCase):
    def test_compute_accuracy(self):
        preds = ["mangan", "pinaq", "tulung"]
        gts = ["mangan", "pinaq", "beli"]
        acc = compute_accuracy(preds, gts)
        self.assertAlmostEqual(acc, 0.6667, places=3)

    def test_compute_precision_recall_f1(self):
        preds = ["a", "b", "c"]
        gts = ["a", "b", "c"]
        prf = compute_precision_recall_f1(preds, gts)
        self.assertEqual(prf["precision"], 1.0)
        self.assertEqual(prf["recall"], 1.0)
        self.assertEqual(prf["f1_score"], 1.0)

    def test_error_analyzer_categories(self):
        analyzer = ErrorAnalyzer()
        # Exact match -> Correct
        self.assertEqual(
            analyzer.classify_error("mangan", "mangan", "mangan"),
            ErrorCategory.CORRECT,
        )
        # Gold is not in lexicon -> OOV
        self.assertEqual(
            analyzer.classify_error("unknown", "unk", "nonexistent_lemma_xyz"),
            ErrorCategory.OOV_ERROR,
        )

    def test_evaluator_batch(self):
        evaluator = BenchmarkEvaluator()
        report = evaluator.evaluate(
            predictions=["mangan", "pinaq"],
            ground_truth=["mangan", "pinaq"],
            surfaces=["mangan", "tepinaq"],
        )
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.total_samples, 2)
        md = report.summary_markdown()
        self.assertIn("Accuracy", md)


if __name__ == "__main__":
    unittest.main()
