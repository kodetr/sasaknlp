"""
Merge harvested entries from Balai Bahasa Provinsi NTB into SasakNLP core lexicon.
"""

import json
from pathlib import Path

def merge_lexicon():
    source_path = Path("datasets/sasaklex/kamus_balai_bahasa_ntb.json")
    core_lex_path = Path("src/sasaknlp/lexicon/data/sasaklex.json")
    default_lex_path = Path("datasets/sasaklex/default_lexicon.json")

    with open(source_path, "r", encoding="utf-8") as f:
        bb_entries = json.load(f)

    with open(core_lex_path, "r", encoding="utf-8") as f:
        core_lex = json.load(f)

    existing_words = {e["word"].lower(): e for e in core_lex}
    start_id = len(core_lex) + 1

    added_count = 0
    for item in bb_entries:
        lemma = item.get("lemma", "").strip().lower()
        # Keep clean single-word base lemmas
        if lemma and " " not in lemma and lemma.isalpha() and len(lemma) >= 2:
            if lemma not in existing_words:
                entry_id = f"SKL{start_id:04d}"
                start_id += 1
                new_entry = {
                    "id": entry_id,
                    "word": lemma,
                    "lemma": lemma,
                    "pos": "GENERAL",
                    "meaning_id": item.get("meaning_id", "").strip(),
                    "dialect": "general",
                    "morphology": {
                        "prefix": None,
                        "infix": None,
                        "suffix": None
                    },
                    "source": "balai_bahasa_provinsi_ntb_sasambo",
                    "frequency": 100
                }
                core_lex.append(new_entry)
                existing_words[lemma] = new_entry
                added_count += 1

    print(f"Added {added_count} verified lemmas from Balai Bahasa NTB.")
    print(f"Total entries in SasakNLP lexicon: {len(core_lex)}")

    # Sort alphabetically by lemma
    core_lex.sort(key=lambda x: x["lemma"])

    # Write back to core lexicon
    with open(core_lex_path, "w", encoding="utf-8") as f:
        json.dump(core_lex, f, ensure_ascii=False, indent=2)
    print(f"Updated {core_lex_path}")

    # Write back to default lexicon
    with open(default_lex_path, "w", encoding="utf-8") as f:
        json.dump(core_lex, f, ensure_ascii=False, indent=2)
    print(f"Updated {default_lex_path}")

if __name__ == "__main__":
    merge_lexicon()
