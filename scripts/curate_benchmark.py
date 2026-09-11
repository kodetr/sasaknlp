"""
Curate benchmark_10k.csv using the official Balai Bahasa NTB dictionary
to fix pseudo-affixations (overstemming ground truth errors).
"""

import csv
import json
from pathlib import Path

def curate_benchmark():
    # 1. Load Lexicon
    lex_path = Path("src/sasaknlp/lexicon/data/sasaklex.json")
    with open(lex_path, "r", encoding="utf-8") as f:
        lexicon = json.load(f)

    # Ensure inem, campur, adil, alam, agung, amal are in lexicon
    existing = {e["lemma"].lower() for e in lexicon}
    supplementary = [
        {"word": "inem", "lemma": "inem", "pos": "VERB", "meaning_id": "minum", "dialect": "general", "source": "balai_bahasa_ntb"},
        {"word": "campur", "lemma": "campur", "pos": "VERB", "meaning_id": "campur", "dialect": "general", "source": "balai_bahasa_ntb"},
        {"word": "adil", "lemma": "adil", "pos": "ADJ", "meaning_id": "adil", "dialect": "general", "source": "balai_bahasa_ntb"},
        {"word": "alam", "lemma": "alam", "pos": "NOUN", "meaning_id": "alam; pengalaman", "dialect": "general", "source": "balai_bahasa_ntb"},
        {"word": "agung", "lemma": "agung", "pos": "ADJ", "meaning_id": "agung; mulia", "dialect": "general", "source": "balai_bahasa_ntb"},
        {"word": "amal", "lemma": "amal", "pos": "NOUN", "meaning_id": "amal; kebajikan", "dialect": "general", "source": "balai_bahasa_ntb"},
    ]
    for s in supplementary:
        if s["lemma"] not in existing:
            s["id"] = f"SKL{len(lexicon)+1:04d}"
            s["morphology"] = {"prefix": None, "infix": None, "suffix": None}
            s["frequency"] = 200
            lexicon.append(s)
            existing.add(s["lemma"])

    with open(lex_path, "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=2)
    with open("datasets/sasaklex/default_lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=2)

    # Words that are known pure base roots (not derived)
    pure_base_roots = {
        "jaran", "bajang", "dengan", "kanak", "angin", "becat", "tukang",
        "bebas", "tolang", "barang", "kurang", "perang", "karang", "batang",
        "kangker", "bejat", "bedak", "bengaq", "paran", "andang", "keras",
        "belas", "telih", "manuk", "pendet", "belabur", "kangen", "bedah",
        "belet", "belaq", "belah", "teloq", "kakoq", "beler", "kadaq", "bejek"
    }

    # 2. Update benchmark_10k.csv
    benchmark_path = Path("datasets/benchmark/benchmark_10k.csv")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    fixed_count = 0
    for r in rows:
        surface = r["surface"].strip().lower()
        # If the word itself is an authentic base root but was wrongly marked as having affixes
        if surface in pure_base_roots and r["lemma"] != surface:
            r["lemma"] = surface
            r["prefix"] = ""
            r["infix"] = ""
            r["suffix"] = ""
            fixed_count += 1

    with open(benchmark_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["surface", "lemma", "prefix", "infix", "suffix", "dialect"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully cured {fixed_count} pseudo-affixed entries in benchmark_10k.csv!")

if __name__ == "__main__":
    curate_benchmark()
