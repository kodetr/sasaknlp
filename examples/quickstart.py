#!/usr/bin/env python3
"""SasakNLP Quickstart Example: Demonstrates basic text processing, tokenization, and stemming."""

from sasaknlp import SasakNLP


def main() -> None:
    # 1. Initialize the NLP pipeline
    nlp = SasakNLP()

    # 2. Input text in Bahasa Sasak
    sample_text = "Tiyang mangan nasiq bareng-bareng kance baturne."

    print("=" * 60)
    print("SasakNLP Quickstart Pipeline Demo")
    print("=" * 60)
    print(f"Raw Input Text : {sample_text}")

    # 3. Process the text
    result = nlp.process(sample_text)

    print(f"Normalized Text: {result.normalized_text}")
    print(f"Detected Dialect: {result.dialect}")
    print(f"Token Count    : {len(result.tokens)}")
    print(f"Tokens         : {result.tokens}")
    print(f"Lemmas         : {result.lemmas}")

    print("\nDetailed Token Analyses:")
    for a in result.analyses:
        print(f"  Word : {a.surface_form:15} -> Root: {a.lemma:10} [Rule: {a.rule_applied or 'none':25}, Conf: {a.confidence:.2f}]")

    # 4. Direct word stemming
    print("\nDirect Word Stemming:")
    words = ["tepinaq", "tulungang", "kelororan", "bareng-bareng"]
    for w in words:
        lemma = nlp.stem(w)
        print(f"  stem('{w}') -> '{lemma}'")


if __name__ == "__main__":
    main()
