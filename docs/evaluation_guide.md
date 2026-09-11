# Evaluation & Scientific Benchmarking Guide

## Overview

SasakNLP includes a specialized scientific evaluation module designed for reproducibility, academic publishing, and systematic error tracking in low-resource NLP research.

---

## 1. Benchmark CSV Format

Benchmark datasets must follow the standardized 6-column CSV structure:

```csv
surface,lemma,prefix,infix,suffix,dialect
mangan,mangan,,,,general
tepinaq,pinaq,te,,,general
tulungang,tulung,,,ang,general
baturne,batur,,,ne,general
kaken,kaken,,,,selaparang
```

---

## 2. Evaluation Metrics

The `BenchmarkEvaluator` computes:

- **Accuracy**: Proportion of exact matches between predicted and ground-truth lemmas.
- **Macro Precision, Recall, and F1**: Unweighted average across all unique lemma classes.
- **Weighted F1**: Average weighted by class support (frequency).
- **Error Taxonomy Breakdown**:
  - `Correct`: Prediction matches gold standard.
  - `Overstemming`: Stemmer removed more characters than the legitimate root.
  - `Understemming`: Stemmer failed to remove all affixes.
  - `Incorrect Lemma`: Predicted lemma belongs to an entirely different root.
  - `OOV Error`: Target word is absent from dictionary.
  - `Dialect Error`: Error caused by dialectal variation.

---

## 3. Running Evaluations

### From Python
```python
from sasaknlp.evaluation import BenchmarkEvaluator
from sasaknlp import SasakStemmer

evaluator = BenchmarkEvaluator()
stemmer = SasakStemmer()

report = evaluator.evaluate_csv("path/to/benchmark.csv", stemmer=stemmer)
print(report.summary_markdown())
```

### From CLI
```bash
sasaknlp evaluate --benchmark datasets/benchmark/synthetic_benchmark.csv
```
