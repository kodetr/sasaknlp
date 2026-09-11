"""Standardized benchmark evaluator for SasakNLP models."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from sasaknlp.evaluation.error_analysis import ErrorAnalyzer
from sasaknlp.evaluation.metrics import compute_accuracy, compute_precision_recall_f1
from sasaknlp.stemmer.stemmer import SasakStemmer


@dataclass
class EvaluationReport:
    """Comprehensive evaluation report data structure."""
    total_samples: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    weighted_f1: float
    error_distribution: Dict[str, Dict[str, Any]]
    error_samples: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "total_samples": self.total_samples,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "weighted_f1": self.weighted_f1,
            "error_distribution": self.error_distribution,
            "error_samples": self.error_samples,
        }

    def summary_markdown(self) -> str:
        """Generate formatted Markdown summary table of evaluation results."""
        lines = [
            "# SasakNLP Benchmark Evaluation Report",
            "",
            "## Primary Metrics",
            "",
            "| Metric | Value |",
            "| --- | --- |",
            f"| Total Test Samples | {self.total_samples} |",
            f"| Accuracy | {self.accuracy * 100:.2f}% |",
            f"| Macro Precision | {self.precision * 100:.2f}% |",
            f"| Macro Recall | {self.recall * 100:.2f}% |",
            f"| Macro F1 Score | {self.f1_score * 100:.2f}% |",
            f"| Weighted F1 Score | {self.weighted_f1 * 100:.2f}% |",
            "",
            "## Error Taxonomy Distribution",
            "",
            "| Error Category | Count | Percentage |",
            "| --- | --- | --- |",
        ]
        for cat, stats in self.error_distribution.items():
            lines.append(f"| {cat} | {stats['count']} | {stats['percentage']:.2f}% |")

        if self.error_samples:
            lines.extend([
                "",
                "## Error Sample Details (Top 10)",
                "",
                "| Surface | Predicted | Ground Truth | Dialect | Error Category |",
                "| --- | --- | --- | --- | --- |",
            ])
            for s in self.error_samples[:10]:
                lines.append(
                    f"| {s['surface']} | {s['predicted']} | {s['ground_truth']} | {s['dialect']} | {s['error_category']} |"
                )

        return "\n".join(lines)


class BenchmarkEvaluator:
    """Evaluates stemmers and morphological analyzers on standard benchmark datasets."""

    def __init__(self, error_analyzer: Optional[ErrorAnalyzer] = None) -> None:
        self.error_analyzer = error_analyzer or ErrorAnalyzer()

    def evaluate(
        self,
        predictions: List[str],
        ground_truth: List[str],
        surfaces: Optional[List[str]] = None,
        dialects: Optional[List[str]] = None,
    ) -> EvaluationReport:
        """Evaluate predictions against ground truth labels."""
        acc = compute_accuracy(predictions, ground_truth)
        prf = compute_precision_recall_f1(predictions, ground_truth)
        err_analysis = self.error_analyzer.analyze_batch(
            surfaces=surfaces or predictions,
            predictions=predictions,
            ground_truth=ground_truth,
            dialects=dialects,
        )

        return EvaluationReport(
            total_samples=len(ground_truth),
            accuracy=acc,
            precision=prf["precision"],
            recall=prf["recall"],
            f1_score=prf["f1_score"],
            weighted_f1=prf["weighted_f1"],
            error_distribution=err_analysis["error_distribution"],
            error_samples=err_analysis["error_samples"],
        )

    def evaluate_csv(
        self,
        csv_path: Union[str, Path],
        stemmer: Optional[SasakStemmer] = None,
    ) -> EvaluationReport:
        """Load benchmark CSV, run stemmer predictions, and evaluate performance.

        Expected CSV format:
            surface,lemma,prefix,infix,suffix,dialect
        """
        active_stemmer = stemmer or SasakStemmer()
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"Benchmark CSV not found at: {path}")

        surfaces: List[str] = []
        ground_truth: List[str] = []
        dialects: List[str] = []

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s = row.get("surface", "").strip()
                g = row.get("lemma", "").strip()
                d = row.get("dialect", "general").strip()
                if s and g:
                    surfaces.append(s)
                    ground_truth.append(g)
                    dialects.append(d)

        predictions = active_stemmer.stem_tokens(surfaces)

        return self.evaluate(
            predictions=predictions,
            ground_truth=ground_truth,
            surfaces=surfaces,
            dialects=dialects,
        )
