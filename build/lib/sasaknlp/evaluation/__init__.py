"""Evaluation module for SasakNLP."""

from sasaknlp.evaluation.error_analysis import ErrorAnalyzer
from sasaknlp.evaluation.evaluator import BenchmarkEvaluator, EvaluationReport
from sasaknlp.evaluation.metrics import (
    compute_accuracy,
    compute_precision_recall_f1,
)

__all__ = [
    "BenchmarkEvaluator",
    "EvaluationReport",
    "ErrorAnalyzer",
    "compute_accuracy",
    "compute_precision_recall_f1",
]
