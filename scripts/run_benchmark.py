#!/usr/bin/env python3
"""CLI utility script to run SasakNLP benchmark evaluation."""

import argparse
import sys
from pathlib import Path

from sasaknlp.evaluation import BenchmarkEvaluator
from sasaknlp.stemmer import SasakStemmer


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SasakNLP benchmark evaluation suite.")
    parser.add_argument(
        "--file",
        "-f",
        default="datasets/benchmark/synthetic_benchmark.csv",
        help="Path to benchmark CSV dataset file",
    )
    parser.add_argument(
        "--dialect",
        "-d",
        default="general",
        help="Target dialect mode",
    )
    args = parser.parse_args()

    csv_path = Path(args.file)
    if not csv_path.exists():
        print(f"Error: File '{csv_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    stemmer = SasakStemmer(dialect=args.dialect)
    evaluator = BenchmarkEvaluator()
    report = evaluator.evaluate_csv(csv_path, stemmer=stemmer)

    print(report.summary_markdown())


if __name__ == "__main__":
    main()
