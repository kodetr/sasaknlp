# SasakNLP: Research-Grade Low-Resource Language NLP Toolkit

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 69 passed](https://img.shields.io/badge/tests-69%20passed-brightgreen.svg)]()
[![Code Style: Clean Architecture](https://img.shields.io/badge/architecture-clean%20%2F%20solid-purple.svg)]()

**SasakNLP** is an open-source Natural Language Processing (NLP) and morphological processing toolkit specifically engineered for **Bahasa Sasak** (*Basa Sasak*), an Austronesian low-resource regional language spoken by approximately 3 million people on the island of Lombok, Indonesia.

Unlike standard rule-based heuristic stemmers, SasakNLP employs a **Dictionary-Enhanced Rule-Based Architecture** featuring multi-candidate morphological generation, lexicon validation, multi-factor candidate ranking, and a dialect-aware framework designed for scientific reproducibility and academic research.

---

## 🔬 Research Focus & Architectural Innovation

Low-resource regional language NLP typically suffers from severe understemming, overstemming, unverified rule assumptions, and dialect conflation. SasakNLP resolves these challenges through a systematic 6-stage pipeline:

```text
               ┌───────────────────────────────┐
               │          INPUT TEXT           │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │      TEXT NORMALIZATION       │
               │   (NFC, Glottals, Quotes)     │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │         TOKENIZATION          │
               │  (Reduplications, Enclitics)  │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │    DIALECT CONTEXTUALIZATION  │
               │ (Markers: Selaparang, Ngeno)  │
               └──────────────┬────────────────┘
                              │
               ┌──────────────┴───────────────┐
               ▼                              ▼
      [Direct Lexicon Lookup]        [Rule Morphological Engine]
       (Is word already root?)                    │
               │                                  ▼
               │                     [Candidate Generation]
               │                      • Prefix rules (te-, pe-, N-)
               │                      • Suffix rules (-an, -ang, -ne)
               │                      • Infix rules (-in-, -um-)
               │                      • Circumfixes (pe-...-an, te-...-ang)
               │                      • Reduplications (kata-kata, kata kata)
               │                                  │
               │                                  ▼
               │                     [Dictionary Validation]
               │                      • EXACT_MATCH
               │                      • PARTIAL_MATCH
               │                      • OOV (Out-Of-Vocabulary)
               │                                  │
               │                                  ▼
               │                     [Candidate Multi-Criteria Ranker]
               │                      Score = w_lex·S_lex + w_morph·S_morph
               │                            + w_conf·S_conf + w_freq·S_freq
               │                            + w_dial·S_dial
               │                                  │
               └──────────────┬───────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │       STRUCTURED OUTPUT       │
               │ (Lemmas, Affixes, Confidence) │
               └───────────────────────────────┘
```

---

## ✨ Features

- **High-Accuracy Morphological Processing**: Supports inflectional prefixes (`te-`), nominalizers (`pe-`), nasal morphophonemics (`N-` $\rightarrow$ `m-`, `n-`, `ng-`, `ny-`), suffixes (`-an`, `-ang`, `-in`), pronominal enclitics (`-ne`, `-ku`, `-mu`), infixes (`-in-`, `-um-`), and circumfixes (`ka-...-an`, `te-...-ang`).
- **Comprehensive Reduplication Handling**: Resolves full hyphenated reduplications (`bareng-bareng`), spaced reduplications (`bareng bareng`), affixed reduplications (`bareng-barengan`), and partial reduplication (*dwipurwa*).
- **SasakLex Dictionary**: In-memory hash indexing and fast Prefix Trie ($O(L)$) for instant lookup and morphological validation.
- **Dialect-Aware Architecture**: Handles dialectal taxonomy including *Menu-Meni* (Selaparang / East Lombok), *Ngeno-Ngene* (Central West), *Mriak-Mriku* (South Central), *Ngeto-Ngete* (Northeast), and *Kuto-Kute* (North/Bayan).
- **Declarative Rule Configuration**: Affix rules and phonological mappings are defined in transparent JSON configuration files, enabling linguistic adaptation without modifying engine code.
- **Scientific Evaluation Suite**: Standardized benchmark evaluator computing Accuracy, Macro/Weighted Precision, Recall, F1, and a 6-tier linguistic error taxonomy (`Correct`, `Overstemming`, `Understemming`, `Incorrect Lemma`, `OOV Error`, `Dialect Error`).
- **Zero Heavy Runtime Dependencies**: Pure Python standard library implementation for maximum speed, portability, and instant installation.
- **CLI & Python API**: Unified interfaces for interactive command-line usage and programmatic scripts.

---

## 📦 Installation

### From Source (Development)

```bash
git clone https://github.com/sasaknlp/sasaknlp.git
cd sasaknlp
pip install -e .
```

### With Developer Dependencies

```bash
pip install -e ".[dev]"
```

---

## 🚀 Quickstart

### 1. Python API

```python
from sasaknlp import SasakNLP

# Initialize default pipeline
nlp = SasakNLP()

# Process full sentence
result = nlp.process("Tiyang mangan nasiq bareng-bareng kance baturne.")

print("Normalized Text :", result.normalized_text)
print("Detected Dialect:", result.dialect)
print("Tokens          :", result.tokens)
print("Lemmas          :", result.lemmas)
```

**Output:**
```text
Normalized Text : tiyang mangan nasiq bareng-bareng kance baturne.
Detected Dialect: selaparang
Tokens          : ['tiyang', 'mangan', 'nasiq', 'bareng-bareng', 'kance', 'baturne']
Lemmas          : ['tiyang', 'mangan', 'nasiq', 'bareng', 'kance', 'batur']
```

### 2. Direct Stemming & Morphological Analysis

```python
from sasaknlp import MorphologicalAnalyzer, SasakStemmer

stemmer = SasakStemmer()
print(stemmer.stem("tepinaq"))      # -> 'pinaq'
print(stemmer.stem("tulungang"))    # -> 'tulung'
print(stemmer.stem("kelororan"))    # -> 'keloror'
print(stemmer.stem("kasolahan"))    # -> 'solah'
print(stemmer.stem("baturne"))      # -> 'batur'

analyzer = MorphologicalAnalyzer()
res = analyzer.analyze("tulungang")
print(res.to_dict())
```

**Structured Analysis:**
```json
{
  "surface_form": "tulungang",
  "lemma": "tulung",
  "prefix": null,
  "infix": null,
  "suffix": "ang",
  "rule_applied": "transitive_ang",
  "dialect": "general",
  "confidence": 0.9624,
  "reduplication": null,
  "is_oov": false
}
```

---

## 💻 Command Line Interface (CLI)

The package provides the `sasaknlp` command:

```bash
# 1. Stem a single word
sasaknlp stem "tepinaq"
# Output:
# Input: tepinaq
# Lemma: pinaq
# Rule: passive_te
# Confidence: 0.9654

# 2. Analyze detailed morphology
sasaknlp analyze "kelororan"

# 3. Process a full sentence
sasaknlp process "Tiyang mangan nasiq bareng-bareng"

# 4. Search and look up dictionary entries
sasaknlp lexicon lookup "mangan"
sasaknlp lexicon search "ba"

# 5. Run benchmark evaluation
sasaknlp evaluate --benchmark datasets/benchmark/synthetic_benchmark.csv
```

---

## 📊 Scientific Benchmark Evaluation

SasakNLP includes a built-in evaluator that scores model outputs against standardized 6-column benchmark datasets:

```bash
python scripts/run_benchmark.py --file datasets/benchmark/synthetic_benchmark.csv
```

**Evaluation Report Output:**
```markdown
# SasakNLP Benchmark Evaluation Report

## Primary Metrics

| Metric | Value |
| --- | --- |
| Total Test Samples | 20 |
| Accuracy | 95.00% |
| Macro Precision | 93.75% |
| Macro Recall | 93.75% |
| Macro F1 Score | 93.75% |
| Weighted F1 Score | 95.00% |

## Error Taxonomy Distribution

| Error Category | Count | Percentage |
| --- | --- | --- |
| Correct | 19 | 95.00% |
| Overstemming | 0 | 0.00% |
| Understemming | 0 | 0.00% |
| Incorrect Lemma | 1 | 5.00% |
| OOV Error | 0 | 0.00% |
| Dialect Error | 0 | 0.00% |
```

---

## 🗂 Repository Structure

```text
library-sasak/
├── pyproject.toml              # Build & packaging configuration
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Community code of conduct
├── requirements.txt            # Minimal runtime dependencies
├── requirements-dev.txt        # Development dependencies
│
├── src/
│   └── sasaknlp/
│       ├── core/               # Pipeline orchestrator, config, and data types
│       ├── tokenizer/          # Word & sentence boundary tokenizers
│       ├── normalization/      # Unicode, glottal apostrophe, and casefold normalizer
│       ├── lexicon/            # SasakLex manager, loader, PrefixTrie, and data
│       ├── morphology/         # Rule engine, candidate generator, analyzer
│       │   └── rules/          # Prefix, suffix, infix, circumfix, reduplication
│       ├── stemmer/            # Dictionary validator, ranker, and SasakStemmer
│       ├── dialect/            # Dialect taxonomy manager and marker detector
│       ├── evaluation/         # Metrics, error analyzer, benchmark evaluator
│       └── cli/                # Command-line interface subcommands
│
├── datasets/
│   ├── sasaklex/               # Base lexicon reference files
│   └── benchmark/              # Benchmark evaluation datasets (CSV)
│
├── examples/
│   ├── quickstart.py           # End-to-end pipeline usage
│   ├── morphological_analysis.py # In-depth morphological candidate inspection
│   └── benchmark_evaluation.py # Academic evaluation script
│
├── docs/                       # Technical & linguistic guides
│   ├── installation.md
│   ├── usage.md
│   ├── lexicon_guide.md
│   ├── morphological_rules.md
│   ├── dialect_guide.md
│   └── evaluation_guide.md
│
├── tests/                      # 69 Unit tests covering all core modules
└── scripts/                    # Automation and evaluation scripts
```

---

## 🧪 Running Tests

Execute the test suite using `unittest` or `pytest`:

```bash
# Using Python's built-in test runner:
python3 -m unittest discover -s tests -v

# Or with pytest:
pytest tests -v
```

All 69 unit tests execute in under 0.05 seconds with 100% pass rate.

---

## 📖 Citation

If you use **SasakNLP** in your research, computational linguistics publications, or low-resource language benchmarks, please cite:

```bibtex
@software{sasaknlp2026,
  author = {SasakNLP Contributors},
  title = {SasakNLP: Research-Grade Natural Language Processing and Morphological Toolkit for Bahasa Sasak},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/sasaknlp/sasaknlp}
}
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
