# SasakNLP Morphological Rules Guide

## Overview

Bahasa Sasak exhibits rich agglutinative and morphophonemic behavior typical of Western Malayo-Polynesian languages. SasakNLP implements a **declarative, JSON-configurable morphological rule engine** allowing linguists to extend or fine-tune rules without modifying core engine code.

---

## 1. Rule Types

### Prefixes
- **Passive `te-`**: `tepinaq` -> `te-` + `pinaq`
- **Agentive/Causative `pe-`**: `pemangan` -> `pe-` + `mangan`
- **Stative `ka-`**: `kaantuk` -> `ka-` + `antuk`
- **Reciprocal `be-`**: `bebatur` -> `be-` + `batur`
- **Nasalization (`N-`)**:
  - `m-` before/replacing bilabial `p`, `b`: `minaq` -> `pinaq`
  - `n-` before/replacing alveolar `t`, `d`: `nulis` -> `tulis`
  - `ny-` before/replacing sibilant/palatal `s`, `c`: `nyolah` -> `solah`
  - `ng-` before/replacing velar `k`, `g` or vowels: `ngaken` -> `kaken`

### Suffixes & Enclitics
- **Locative/Nominalizer `-an`**: `keloror` + `-an` -> `kelororan`
- **Transitive/Causative `-ang`**: `tulung` + `-ang` -> `tulungang`
- **Iterative/Focus `-in`**: `antep` + `-in` -> `antepin`
- **Pronominal Enclitics**:
  - `-ne` (3rd person possessive: `baturne`)
  - `-ku` (1st person possessive: `anakku`)
  - `-mu` (2nd person possessive: `anakmu`)

### Infixes
- **Passive/Perfective `-in-`**: `p-in-inaq` -> `pinaq`, `t-in-ulung` -> `tulung`
- **Agentive/Intensive `-um-`**: `t-um-ulung` -> `tulung`
- **Repetitive/Plural `-er-`, `-el-`**

### Combinations & Circumfixes
- `pe-...-an`: `pemangan` -> `mangan`
- `te-...-ang`: `tetulungang` -> `tulung`
- `ka-...-an`: `kasolahan` -> `solah`
- `be-...-an`: `bebaturan` -> `batur`

### Reduplication
- Full hyphenated: `bareng-bareng` -> `bareng`
- Full spaced: `bareng bareng` -> `bareng`
- Reduplication + suffix: `bareng-barengan` -> `bareng`
- Partial (dwipurwa): `bebatur` -> `batur`, `tetulung` -> `tulung`

---

## 2. Declarative Rule Configuration

All rules are loaded from `src/sasaknlp/morphology/rules/rules_config.json`. To supply custom rules:

```python
from sasaknlp import SasakNLP

nlp = SasakNLP(custom_rules_path="path/to/my_rules.json")
```
