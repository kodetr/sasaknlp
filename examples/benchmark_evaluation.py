#!/usr/bin/env python3
"""SasakNLP Benchmark Evaluation Script: Demonstrating scientific metric calculation and error analysis."""

from pathlib import Path

from sasaknlp.evaluation import BenchmarkEvaluator
from sasaknlp.stemmer import SasakStemmer


def main() -> None:
    benchmark_path = Path(__file__).parent.parent / "datasets" / "benchmark" / "synthetic_benchmark.csv"

    print("=" * 70)
    print("SasakNLP Scientific Benchmark Evaluation")
    print("=" * 70)
    print(f"Loading Benchmark: {benchmark_path.resolve()}\n")

    evaluator = BenchmarkEvaluator()
    stemmer = SasakStemmer()

    report = evaluator.evaluate_csv(benchmark_path, stemmer=stemmer)

    print(report.summary_markdown())


if __name__ == "__main__":
    main()
