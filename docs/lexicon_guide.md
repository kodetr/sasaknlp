# SasakLex: Lexicon Management Guide

## Overview

**SasakLex** is the lexical dictionary backing SasakNLP's validation and ranking phases. It stores verified lemmas, grammatical categories, Indonesian glosses, frequency distributions, and dialect annotations.

---

## Data Schema

Every entry in `SasakLex` conforms to the following JSON format:

```json
{
  "id": "SKL00001",
  "word": "mangan",
  "lemma": "mangan",
  "pos": "VERB",
  "meaning_id": "makan",
  "dialect": "general",
  "morphology": {
    "prefix": null,
    "infix": null,
    "suffix": null
  },
  "source": "kamus_bahasa_sasak_indonesia_balai_bahasa",
  "frequency": 1250
}
```

### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `id` | `string` | Unique identifier (e.g. `SKL00001`). |
| `word` | `string` | Surface form or headword. |
| `lemma` | `string` | Base morphological root. |
| `pos` | `string` | Part-of-speech tag (`VERB`, `NOUN`, `ADJ`, `ADV`, `PRON`, etc.). |
| `meaning_id` | `string` | Meaning in Bahasa Indonesia. |
| `dialect` | `string` | Regional dialect: `general`, `selaparang`, `ngeno_ngene`, etc. |
| `morphology` | `dict` | Affix metadata (`prefix`, `infix`, `suffix`). |
| `source` | `string` | Scholarly source citation. |
| `frequency` | `int` | Corpus occurrence count. |

---

## How to Add Custom Lexicons

You can load your own JSON or CSV lexicon file into the `SasakLexManager`:

```python
from sasaknlp import SasakLexManager

# Initialize with custom lexicon
lexicon = SasakLexManager(data_path="path/to/my_lexicon.json")

# Or add entries dynamically
from sasaknlp.core.types import LexiconEntry

entry = LexiconEntry(
    id="CUSTOM001",
    word="umbaq",
    lemma="umbaq",
    pos="VERB",
    meaning_id="menggendong anak",
    dialect="general",
    source="balai_bahasa_ntb",
    frequency=190,
)
lexicon.add_entry(entry)
```
