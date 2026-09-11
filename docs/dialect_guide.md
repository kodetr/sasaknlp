# Dialect-Aware Architecture Guide

## Overview

Bahasa Sasak exhibits prominent dialectal variation across Lombok Island. In Indonesian computational linguistics (Teeuw, Mahsun), Sasak dialects are traditionally categorized into 5 major clusters based on distinct lexical shibboleths (isoglosses):

1. **Menu-Meni (Selaparang / East & Central East Lombok)**: Characterized by the 'menu-meni' (begini-begitu) shibboleth and refined *alus* speech registers (*tiyang*, *kaken*, *ngonang*).
2. **Ngeno-Ngene (Central West Lombok)**: Characterized by 'ngeno-ngene' (begini-begitu).
3. **Mriak-Mriku (South Central Lombok)**: Characterized by 'mriak-mriku' (kemari-kesana).
4. **Ngeto-Ngete (Northeast Lombok)**: Characterized by 'ngeto-ngete'.
5. **Kuto-Kute (North Lombok / Bayan)**: Retaining older Austronesian structural features.
6. **General Sasak**: Standard cross-dialectal baseline.

---

## Dialect Processing in SasakNLP

SasakNLP supports:
```python
from sasaknlp import SasakNLP, SasakStemmer

# 1. Automatic dialect detection based on diagnostic lexical markers
nlp_auto = SasakNLP(dialect="auto")

# 2. Explicit dialect targeting
nlp_selaparang = SasakNLP(dialect="selaparang")
nlp_general = SasakNLP(dialect="general")
```

### Extending Dialect Rules

To register new dialect definitions or update diagnostic markers:

```python
from sasaknlp import DialectManager

manager = DialectManager()
manager.register_dialect(
    dialect_code="my_dialect",
    name="Custom Regional Dialect",
    markers=["word_a", "word_b"],
    description="Custom dialect cluster documentation",
)
```
