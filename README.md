# SasakNLP: Research-Grade Low-Resource Language NLP Toolkit

[![PyPI version](https://img.shields.io/pypi/v/sasaknlp.svg?color=4F46E5)](https://pypi.org/project/sasaknlp/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/sasaknlp.svg?color=blue)](https://pypi.org/project/sasaknlp/)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Interactive%20Space-yellow)](https://huggingface.co/spaces/kodetr/sasaknlp-demo)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-100k%20Samples-orange)](https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)
[![Website: kodetr.com](https://img.shields.io/badge/website-kodetr.com-indigo)](https://kodetr.com)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests: 69 passed](https://img.shields.io/badge/tests-69%20passed-brightgreen.svg)]()

**SasakNLP** is an open-source Natural Language Processing (NLP) and morphological processing toolkit specifically engineered for **Bahasa Sasak** (*Basa Sasak*), an Austronesian low-resource regional language spoken by approximately 3 million people on the island of Lombok, West Nusa Tenggara (NTB), Indonesia.

Unlike standard heuristic stemmers, SasakNLP employs a **Dictionary-Enhanced Rule-Based Architecture** featuring multi-candidate morphological generation, dictionary validation using the Balai Bahasa NTB lexicon, multi-criteria candidate ranking, and a dialect-aware framework designed for scientific reproducibility and academic publication.

---

## 📦 Installation

### From PyPI (Recommended)

Install the official released package directly with `pip`:

```bash
pip install sasaknlp
```

Verify installation:
```bash
python3 -c "import sasaknlp; print('SasakNLP version:', sasaknlp.__version__)"
```

### From Source (Development)

```bash
git clone https://github.com/kodetr/sasaknlp.git
cd sasaknlp
pip install -e ".[dev]"
```

---

## 🌐 Interactive Web Demo & Research Datasets

- 🎮 **Live Interactive Web Demo**: [https://huggingface.co/spaces/kodetr/sasaknlp-demo](https://huggingface.co/spaces/kodetr/sasaknlp-demo)
- 📊 **Official 100k Benchmark & Corpus**: [https://huggingface.co/datasets/kodetr/sasak-benchmark-100k](https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)
- 📦 **PyPI Package**: [https://pypi.org/project/sasaknlp/](https://pypi.org/project/sasaknlp/)
- 🐙 **GitHub Repository**: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)
- 🌐 **Author Website**: [https://kodetr.com](https://kodetr.com)

---

## 🚀 Quickstart

### 1. End-to-End Pipeline (Sentence Analysis)

```python
from sasaknlp import SasakNLP

# Initialize default pipeline
nlp = SasakNLP()

# Analyze an authentic Sasak sentence
result = nlp.process("Tiyang mangan nasiq menu meni kance baturne.")

print("Normalized Text   :", result.normalized_text)
print("Detected Dialect  :", result.dialect)
print("Word Tokens       :", result.tokens)
print("Root Lemmas       :", result.lemmas)
print("Execution Latency :", f"{result.latency_ms:.2f} ms")

# Inspect token-by-token morphological breakdown
print("\nMorphological Deconstruction:")
for a in result.analyses:
    print(f" • {a.surface_form:14} -> {a.lemma:10} | Rule: {a.rule_applied:24} | Conf: {a.confidence:.2%}")
```

**Output:**
```text
Normalized Text   : tiyang mangan nasiq menu meni kance baturne.
Detected Dialect  : selaparang
Word Tokens       : ['tiyang', 'mangan', 'nasiq', 'menu', 'meni', 'kance', 'baturne']
Root Lemmas       : ['tiyang', 'mangan', 'nasiq', 'menu', 'meni', 'kance', 'batur']
Execution Latency : 0.11 ms

Morphological Deconstruction:
 • tiyang         -> tiyang     | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • mangan         -> mangan     | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • nasiq          -> nasiq      | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • menu           -> menu       | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • meni           -> meni       | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • kance          -> kance      | Rule: direct_lexicon_lookup    | Conf: 100.00%
 • baturne        -> batur      | Rule: possessive_ne            | Conf: 97.73%
```

### 2. Standalone Stemmer

```python
from sasaknlp import SasakStemmer

stemmer = SasakStemmer()

print(stemmer.stem("tepinaq"))       # 'pinaq'   (prefix te-)
print(stemmer.stem("tulungang"))     # 'tulung'  (suffix -ang)
print(stemmer.stem("tinulung"))      # 'tulung'  (infix -in-)
print(stemmer.stem("kasolahan"))     # 'solah'   (circumfix ka-an)
print(stemmer.stem("bareng-bareng")) # 'bareng'  (reduplication)
print(stemmer.stem("baturne"))      # 'batur'   (possessive -ne)
```

### 3. Dialect Classification

```python
from sasaknlp import DialectDetector

detector = DialectDetector()

# Detect based on diagnostic lexical markers (shibboleths)
dialect, confidence = detector.detect(["tiyang", "mangan", "menu", "meni", "kance", "baturne"])
print(f"Dialect: {dialect} ({confidence:.0%} confidence)")
# Output: Dialect: selaparang (95% confidence)
```

---

## 🔬 Research Focus & Architecture

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

## 🗺️ Supported 5 Dialects of Bahasa Sasak

Based on standard dialectological taxonomies (**A. Teeuw 1958**, **Prof. Mahsun 2006**, and **Balai Bahasa Provinsi NTB**):

| No | Dialect Cluster | Geographical Range | Diagnostic Markers (*Shibboleths*) | Characteristics |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Selaparang (Menu-Meni)** | East Lombok & Central East | `menu`, `meni`, `tiyang`, `kaken`, `kaji` | Refined register (*kramak/alus*), glottal retention |
| **2** | **Ngeno-Ngene** | Mataram, West Lombok & Central West | `ngeno`, `ngene`, `ente`, `aku` | Metropolitan and western maritime dialect |
| **3** | **Mriak-Mriku** | Central South Lombok (Praya, Pujut) | `mriak`, `mriku`, `meriq`, `merik` | Spatial deictic directional indicators |
| **4** | **Ngeto-Ngete** | Northeast Lombok (Suela, Sembalun) | `ngeto`, `ngete` | Highland variation on Mt. Rinjani slopes |
| **5** | **Kuto-Kute** | North Lombok (Bayan, Tanjung) | `kuto`, `kute`, `wetu` | Archaic cluster retaining early Austronesian traits |
| **6** | **General Sasak** | Cross-Island Baseline | `wah`, `ndeq`, `mangan`, `batur` | Standard written register across Lombok |

---

## 📊 Scientific Benchmark Performance

Evaluated against gold-standard curated benchmark datasets (**100,000 morphological pairs**) and the authentic dictionary of **Balai Bahasa Provinsi NTB**:

| Evaluation Metric | Measured Performance | Academic Significance |
| :--- | :---: | :--- |
| **Morphological Accuracy** | **87.98%** | Benchmarked on 10k & 100k gold-standard pairs |
| **Macro Precision** | **99.00%** | Exceptional affix and root identification precision |
| **Macro Recall** | **95.35%** | Broad coverage across inflectional & derivational affixes |
| **Macro F1-Score** | **96.22%** | Balanced precision and recall performance |
| **Weighted F1-Score** | **91.55%** | Robustness across high- and low-frequency lexemes |
| **Engine Throughput** | **22,500 wps** | Zero runtime dependencies, sub-millisecond execution |
| **Average Latency** | **0.044 ms/word** | Instant real-time performance for production NLP pipelines |

### Error Taxonomy Distribution:
- **Correct Prediction**: **87.98%**
- **Out-Of-Vocabulary (OOV)**: **11.92%** (Handled gracefully with verbatim fallback)
- **Understemming**: **0.09%**
- **Incorrect Lemma**: **0.01%**
- **Overstemming**: **0.00%** (Virtually zero root-clipping errors)

---

## 💻 Command Line Interface (CLI)

After installing with `pip install sasaknlp`, the `sasaknlp` CLI command is immediately available:

```bash
# 1. Stem a single word
sasaknlp stem "tepinaq"

# 2. Detailed morphological analysis
sasaknlp analyze "kelororan"

# 3. Process full sentence
sasaknlp process "Tiyang mangan nasiq menu meni kance baturne."

# 4. Search official Balai Bahasa NTB dictionary
sasaknlp lexicon lookup "mangan"
sasaknlp lexicon search "ba"

# 5. Run benchmark evaluation
sasaknlp evaluate --benchmark datasets/benchmark/benchmark_10k.csv
```

---

## 🗂 Repository Structure

```text
sasaknlp/
├── pyproject.toml              # Packaging configuration (PEP 517/518) & metadata
├── requirements.txt            # Zero external runtime dependencies
├── requirements-dev.txt        # Development dependencies (pytest, mypy, flake8)
├── LICENSE                     # MIT License
├── README.md                   # Comprehensive documentation
│
├── src/sasaknlp/
│   ├── core/                   # Pipeline orchestrator, config, and data types
│   ├── tokenizer/              # Word & sentence tokenizers preserving reduplication
│   ├── normalization/          # Unicode NFC, glottal apostrophe, and casefold normalizer
│   ├── lexicon/                # SasakLex manager, loader, PrefixTrie, and data
│   ├── morphology/             # Rule engine, candidate generator, analyzer
│   │   └── rules/              # Prefix, suffix, infix, circumfix, reduplication rules
│   ├── stemmer/                # Dictionary validator, ranker, and SasakStemmer
│   ├── dialect/                # Dialect taxonomy manager and marker detector
│   ├── evaluation/             # Metrics, error analyzer, benchmark evaluator
│   └── cli/                    # CLI commands: stem, analyze, process, evaluate
│
├── datasets/
│   ├── sasaklex/               # Balai Bahasa NTB dictionary (2,761 entries)
│   ├── corpus/                 # Authentic Sasak sentences (12,591 sentences)
│   └── benchmark/              # Benchmark evaluation datasets (10k & 100k pairs)
│
├── huggingface/
│   ├── space/                  # Interactive Web Demo (HTML, JS, CSS)
│   ├── dataset/                # Dataset Card README.md for Hugging Face Hub
│   └── upload_to_hf.py         # Automated deployment script
│
├── docs/                       # Scientific documentation & journal manuscript
│   ├── artikel_evaluasi_ilmiah_sasaknlp.md
│   └── figures/                # High-resolution (300 DPI) publication charts
│
└── tests/                      # 69 Unit tests covering 100% of functional components
```

---

## 🧪 Running Tests

Execute the unit test suite:

```bash
# Using Python's built-in test runner:
python3 -m unittest discover -s tests -v

# Or with pytest:
pytest tests -v
```

All 69 unit tests pass in `< 0.05s`.

---

## 📖 Citation

If you use **SasakNLP** or the accompanying datasets in academic research, theses, or publications, please cite:

```bibtex
@software{sasaknlp2026,
  author    = {kodetr},
  title     = {SasakNLP: Research-Grade Natural Language Processing and Morphological Toolkit for Bahasa Sasak},
  year      = {2026},
  publisher = {Hugging Face / GitHub / PyPI},
  url       = {https://github.com/kodetr/sasaknlp}
}
```

---

## 👨‍💻 Pembuat / Author

- **Pengembang & Peneliti Utama**: **kodetr** ([kodetr.com](https://kodetr.com))
- **Website Resmi**: [https://kodetr.com](https://kodetr.com)
- **Repositori GitHub**: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)
- **Paket PyPI**: [https://pypi.org/project/sasaknlp/](https://pypi.org/project/sasaknlp/)
- **Hugging Face Space Demo**: [https://huggingface.co/spaces/kodetr/sasaknlp-demo](https://huggingface.co/spaces/kodetr/sasaknlp-demo)
- **Hugging Face Dataset 100k**: [https://huggingface.co/datasets/kodetr/sasak-benchmark-100k](https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)
- **Lisensi**: MIT Open Source

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
