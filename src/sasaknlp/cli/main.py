"""Command Line Interface for SasakNLP toolkit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from sasaknlp import __version__
from sasaknlp.core.pipeline import SasakNLP
from sasaknlp.evaluation.evaluator import BenchmarkEvaluator
from sasaknlp.lexicon.manager import SasakLexManager


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="sasaknlp",
        description="SasakNLP: Research-Grade Low-Resource Language NLP Toolkit for Bahasa Sasak",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"SasakNLP {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. Stem command
    stem_parser = subparsers.add_parser("stem", help="Stem a Sasak word to its base lemma")
    stem_parser.add_argument("word", help="Sasak word to stem")
    stem_parser.add_argument("--dialect", default="general", help="Target dialect (default: general)")
    stem_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 2. Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Perform morphological analysis on a word")
    analyze_parser.add_argument("word", help="Sasak word to analyze")
    analyze_parser.add_argument("--dialect", default="general", help="Target dialect (default: general)")
    analyze_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 3. Process command (full pipeline)
    process_parser = subparsers.add_parser("process", help="Process text through full NLP pipeline")
    process_parser.add_argument("text", help="Text to process")
    process_parser.add_argument("--dialect", default="auto", help="Dialect mode (auto, general, selaparang, etc.)")
    process_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 4. Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate model against benchmark CSV")
    eval_parser.add_argument("--benchmark", required=True, help="Path to benchmark CSV file")
    eval_parser.add_argument("--json", action="store_true", help="Output evaluation report as JSON")
    eval_parser.add_argument("--dialect", default="general", help="Evaluation dialect mode")

    # 5. Lexicon command
    lex_parser = subparsers.add_parser("lexicon", help="Query the SasakLex dictionary")
    lex_subparsers = lex_parser.add_subparsers(dest="lex_action", help="Lexicon action")

    lookup_p = lex_subparsers.add_parser("lookup", help="Look up a word in SasakLex")
    lookup_p.add_argument("word", help="Word to look up")

    search_p = lex_subparsers.add_parser("search", help="Prefix search in SasakLex")
    search_p.add_argument("prefix", help="Prefix to search for")
    search_p.add_argument("--limit", type=int, default=10, help="Maximum matches to show")

    return parser


def handle_stem(args: argparse.Namespace) -> int:
    """Handle 'stem' subcommand."""
    nlp = SasakNLP(dialect=args.dialect)
    word = args.word
    lemma, cand = nlp.stemmer.stem_with_candidate(word)

    if args.json:
        print(json.dumps(cand.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Input: {word}")
        print(f"Lemma: {lemma}")
        print(f"Rule: {cand.rule_applied}")
        print(f"Confidence: {cand.score:.4f}")
    return 0


def handle_analyze(args: argparse.Namespace) -> int:
    """Handle 'analyze' subcommand."""
    nlp = SasakNLP(dialect=args.dialect)
    analysis = nlp.analyzer.analyze(args.word)

    if args.json:
        print(json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Surface Form : {analysis.surface_form}")
        print(f"Lemma        : {analysis.lemma}")
        print(f"Prefix       : {analysis.prefix or '-'}")
        print(f"Infix        : {analysis.infix or '-'}")
        print(f"Suffix       : {analysis.suffix or '-'}")
        print(f"Rule Applied : {analysis.rule_applied or '-'}")
        print(f"Dialect      : {analysis.dialect}")
        print(f"Confidence   : {analysis.confidence:.4f}")
        print(f"Reduplication: {analysis.reduplication or '-'}")
        print(f"Is OOV       : {analysis.is_oov}")
    return 0


def handle_process(args: argparse.Namespace) -> int:
    """Handle 'process' subcommand."""
    nlp = SasakNLP(dialect=args.dialect)
    result = nlp.process(args.text)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Input Text      : {result.text}")
        print(f"Normalized Text : {result.normalized_text}")
        print(f"Detected Dialect: {result.dialect}")
        print(f"Tokens ({len(result.tokens)})  : {result.tokens}")
        print(f"Lemmas          : {result.lemmas}")
        print("\nMorphological Breakdown:")
        for a in result.analyses:
            affixes = []
            if a.prefix:
                affixes.append(f"pref={a.prefix}")
            if a.infix:
                affixes.append(f"inf={a.infix}")
            if a.suffix:
                affixes.append(f"suf={a.suffix}")
            affix_str = f" [{', '.join(affixes)}]" if affixes else ""
            print(f"  • {a.surface_form:15} -> {a.lemma:12} ({a.rule_applied}){affix_str} [conf={a.confidence:.2f}]")
    return 0


def handle_evaluate(args: argparse.Namespace) -> int:
    """Handle 'evaluate' subcommand."""
    evaluator = BenchmarkEvaluator()
    nlp = SasakNLP(dialect=args.dialect)
    report = evaluator.evaluate_csv(args.benchmark, stemmer=nlp.stemmer)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(report.summary_markdown())
    return 0


def handle_lexicon(args: argparse.Namespace) -> int:
    """Handle 'lexicon' subcommand."""
    lex = SasakLexManager()
    if args.lex_action == "lookup":
        entry = lex.lookup(args.word)
        if entry:
            print(json.dumps(entry.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(f"Word '{args.word}' not found in SasakLex.", file=sys.stderr)
            return 1
    elif args.lex_action == "search":
        entries = lex.search(args.prefix, limit=args.limit)
        print(f"Found {len(entries)} matching entries for prefix '{args.prefix}':")
        for e in entries:
            print(f"  • {e.word} ({e.pos}) - {e.meaning_id} [{e.dialect}]")
    else:
        print("Please specify a lexicon action: lookup or search", file=sys.stderr)
        return 1
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "stem":
        return handle_stem(args)
    elif args.command == "analyze":
        return handle_analyze(args)
    elif args.command == "process":
        return handle_process(args)
    elif args.command == "evaluate":
        return handle_evaluate(args)
    elif args.command == "lexicon":
        return handle_lexicon(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
