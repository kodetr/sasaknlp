#!/usr/bin/env python3
"""Detailed Morphological Analysis demonstration with Candidate Generator and Ranker inspection."""

from sasaknlp import MorphologicalAnalyzer, SasakStemmer, SasakLexManager
from sasaknlp.morphology import CandidateGenerator
from sasaknlp.stemmer import CandidateRanker, DictionaryValidator


def main() -> None:
    print("=" * 70)
    print("SasakNLP In-Depth Morphological Analysis Demo")
    print("=" * 70)

    analyzer = MorphologicalAnalyzer()
    lexicon = SasakLexManager()
    generator = CandidateGenerator()
    validator = DictionaryValidator(lexicon_manager=lexicon)
    ranker = CandidateRanker()

    sample_words = [
        "mangan",       # Base lemma (direct lookup)
        "tepinaq",      # Prefix te-
        "tulungang",    # Suffix -ang
        "kelororan",    # Suffix -an
        "tinulung",     # Infix -in-
        "kasolahan",    # Circumfix ka-...-an
        "bareng-bareng",# Reduplication
        "baturne",      # Enclitic -ne
    ]

    for word in sample_words:
        print(f"\nAnalyzing: '{word}'")
        print("-" * 50)

        # 1. Structured output from high-level analyzer
        analysis = analyzer.analyze(word)
        print(f"Surface Form : {analysis.surface_form}")
        print(f"Lemma        : {analysis.lemma}")
        print(f"Prefix       : {analysis.prefix}")
        print(f"Infix        : {analysis.infix}")
        print(f"Suffix       : {analysis.suffix}")
        print(f"Rule Applied : {analysis.rule_applied}")
        print(f"Confidence   : {analysis.confidence:.4f}")
        print(f"Dialect      : {analysis.dialect}")
        print(f"Is OOV       : {analysis.is_oov}")

        # 2. Inspect candidate generation and scoring internals
        raw_candidates = generator.generate(word)
        validated = validator.validate_all(raw_candidates)
        ranked = ranker.rank_all(validated)

        print(f"\nGenerated Candidates ({len(ranked)}):")
        for i, cand in enumerate(ranked[:3], start=1):
            scores = cand.breakdown_scores
            print(
                f"  [{i}] '{cand.lemma_candidate}' | status={cand.validation_status.value:11} "
                f"| score={cand.score:.3f} (lex={scores.get('s_lex')}, morph={scores.get('s_morph')}) "
                f"| rule={cand.rule_applied}"
            )


if __name__ == "__main__":
    main()
