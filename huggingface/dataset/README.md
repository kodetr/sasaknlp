---
language:
- sas
- id
license: mit
task_categories:
- text-classification
- feature-extraction
tags:
- nlp
- morphology
- sasak
- low-resource-language
- indonesian-languages
- linguistics
- stemmer
pretty_name: Sasak NLP Morphological Benchmark & Authentic Corpus
size_categories:
- 100K<n<1M
configs:
- config_name: benchmark
  data_files:
  - split: train
    path: "benchmark_100k.parquet"
  default: true
- config_name: corpus
  data_files:
  - split: train
    path: "sasak_sentences_large.parquet"
- config_name: lexicon
  data_files:
  - split: train
    path: "kamus_balai_bahasa_ntb.parquet"
dataset_info:
- config_name: benchmark
  features:
  - name: surface
    dtype: string
  - name: lemma
    dtype: string
  - name: prefix
    dtype: string
  - name: infix
    dtype: string
  - name: suffix
    dtype: string
  - name: dialect
    dtype: string
  splits:
  - name: train
    num_examples: 100000
- config_name: corpus
  features:
  - name: id
    dtype: string
  - name: text
    dtype: string
  - name: word_count
    dtype: string
  - name: dialect
    dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_examples: 12591
- config_name: lexicon
  features:
  - name: word
    dtype: string
  - name: lemma
    dtype: string
  - name: pos
    dtype: string
  - name: dialect
    dtype: string
  - name: meaning_id
    dtype: string
  - name: meaning_2
    dtype: string
  - name: example
    dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_examples: 2761
---

# 🌴 SasakNLP: Morphological Benchmark & Authentic Sasak Corpus

Official research dataset accompanying the **SasakNLP** toolkit, developed by **kodetr** ([kodetr.com](https://kodetr.com)). 
Bahasa Sasak is an Austronesian low-resource regional language spoken by approximately 3 million people across Lombok, West Nusa Tenggara (NTB), Indonesia.

- **Website Resmi**: [https://kodetr.com](https://kodetr.com)
- **Repositori GitHub**: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)
- **Web Demo Space**: [https://huggingface.co/spaces/kodetr/sasaknlp-demo](https://huggingface.co/spaces/kodetr/sasaknlp-demo)

## 📂 Dataset Subsets (Configs)

1. **`benchmark`** (`benchmark_100k.parquet` & `.csv`): 100,000 verified morphological test pairs (`surface`, `lemma`, `prefix`, `infix`, `suffix`, `dialect`) curated following Sastrawi-grade purity standards.
2. **`corpus`** (`sasak_sentences_large.parquet` & `.csv`): 12,591 authentic sentences collected from folklore (*Putri Mandalika*, *Dewi Anjani*, *Datu Doyan Nada*), Balai Bahasa NTB examples, and verified regional publications.
3. **`lexicon`** (`kamus_balai_bahasa_ntb.parquet` & `.csv`): 2,761 official lexicon entries harvested from Balai Bahasa Provinsi NTB (*Kamus Terpadu Sasambo*).

## 🚀 Usage with Python `datasets`

```python
from datasets import load_dataset

# 1. Load the benchmark dataset (100,000 pairs)
benchmark = load_dataset("kodetr/sasak-benchmark-100k", "benchmark")
print(benchmark['train'][0])

# 2. Load authentic sentences corpus (12,591 sentences)
corpus = load_dataset("kodetr/sasak-benchmark-100k", "corpus")
print(corpus['train'][0])

# 3. Load Balai Bahasa NTB dictionary
lexicon = load_dataset("kodetr/sasak-benchmark-100k", "lexicon")
print(lexicon['train'][0])
```

## 🛠 Accompanying Toolkit

Install the official Python library:
```bash
pip install sasaknlp
```

Quick example:
```python
from sasaknlp import SasakNLP

nlp = SasakNLP()
res = nlp.process("Tiyang mangan nasiq bareng-bareng kance baturne.")
print(res.lemmas)
```

## 📖 Citation

```bibtex
@software{sasaknlp2026,
  author    = {kodetr},
  title     = {SasakNLP: Research-Grade Natural Language Processing and Morphological Toolkit for Bahasa Sasak},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://github.com/kodetr/sasaknlp}
}
```
