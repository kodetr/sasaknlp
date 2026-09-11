# SasakNLP Usage Guide

SasakNLP provides modular APIs ranging from the high-level `SasakNLP` orchestrator to granular low-level morphological rule engines.

---

## 1. High-Level Pipeline

The `SasakNLP` class coordinates normalization, tokenization, dialect processing, morphological analysis, and stemming in a single call:

```python
from sasaknlp import SasakNLP

# Initialize default pipeline
nlp = SasakNLP()

# Process full sentence
result = nlp.process("Tiyang mangan nasiq bareng-bareng")

print("Raw text       :", result.text)
print("Normalized     :", result.normalized_text)
print("Detected Dialect:", result.dialect)
print("Tokens         :", result.tokens)
print("Lemmas         :", result.lemmas)

# Access individual token analyses
for analysis in result.analyses:
    print(f"{analysis.surface_form:15} -> {analysis.lemma:10} (Rule: {analysis.rule_applied})")
```

---

## 2. Direct Stemming

If you only need root extraction:

```python
from sasaknlp import SasakStemmer

stemmer = SasakStemmer()

# Single word
lemma = stemmer.stem("tepinaq")
print(lemma)  # Output: 'pinaq'

# With candidate metadata
lemma, candidate = stemmer.stem_with_candidate("tulungang")
print("Lemma:", lemma)
print("Rule :", candidate.rule_applied)
print("Score:", candidate.score)
print("Score Breakdown:", candidate.breakdown_scores)
```

---

## 3. Morphological Analysis

To obtain detailed affix decomposition:

```python
from sasaknlp import MorphologicalAnalyzer

analyzer = MorphologicalAnalyzer()

analysis = analyzer.analyze("kelororan")
print("Surface form :", analysis.surface_form)
print("Root lemma   :", analysis.lemma)
print("Prefix       :", analysis.prefix)
print("Infix        :", analysis.infix)
print("Suffix       :", analysis.suffix)
print("Confidence   :", analysis.confidence)
print("Reduplication:", analysis.reduplication)
```

---

## 4. Normalization and Tokenization

For standalone text cleaning and token extraction:

```python
from sasaknlp import SasakNormalizer, SasakTokenizer, SasakSentenceTokenizer

norm = SasakNormalizer()
clean_text = norm.normalize("‘Tiyang mangan’...   bareng-bareng!")
print(clean_text)  # Output: "'tiyang mangan'... bareng-bareng!"

tokenizer = SasakTokenizer()
tokens = tokenizer.tokenize(clean_text, keep_punct=False)
print(tokens)  # Output: ['tiyang', 'mangan', 'bareng-bareng']

sent_tokenizer = SasakSentenceTokenizer()
sentences = sent_tokenizer.tokenize("Tgh. Lalu mangan. Side kaken?")
print(sentences)  # Output: ['Tgh. Lalu mangan.', 'Side kaken?']
```

---

## 5. Command-Line Interface (CLI)

```bash
# Stem a word
sasaknlp stem "tepinaq"

# Analyze morphology
sasaknlp analyze "kelororan"

# Process full sentence
sasaknlp process "tiyang mangan nasiq bareng-bareng"

# Query dictionary
sasaknlp lexicon lookup "mangan"
sasaknlp lexicon search "ba"

# Evaluate benchmark
sasaknlp evaluate --benchmark path/to/benchmark.csv
```
