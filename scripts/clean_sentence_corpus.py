"""
Clean markup artifacts, footnote brackets, and unbalanced quotes from Sasak sentence corpora.
"""

import csv
import json
import re
from pathlib import Path

def sanitize_sentence(text: str) -> str:
    # 1. Remove brackets [ and ]
    t = text.replace('[', '').replace(']', '')
    # 2. Remove tildes ~
    t = t.replace('~', '')
    # 3. Clean spaces
    t = re.sub(r'\s+', ' ', t).strip()
    # 4. Clean unbalanced quotes at start/end
    if t.endswith('"') and t.count('"') % 2 != 0:
        t = t[:-1].strip()
    if t.startswith('"') and t.count('"') % 2 != 0:
        t = t[1:].strip()
    return t

def clean_corpus_file(csv_path: Path, jsonl_path: Path):
    if not csv_path.exists():
        return
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
        
    cleaned_count = 0
    for r in rows:
        old = r['text']
        new = sanitize_sentence(old)
        if new != old:
            r['text'] = new
            r['word_count'] = str(len(new.split()))
            if 'char_count' in r:
                r['char_count'] = str(len(new))
            cleaned_count += 1
            
    # Write back CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    # Write back JSONL
    if jsonl_path.exists():
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
                
    print(f"Cleaned {cleaned_count:,} sentences in {csv_path.name}")

if __name__ == "__main__":
    clean_corpus_file(
        Path("datasets/corpus/sasak_sentences_large.csv"),
        Path("datasets/corpus/sasak_sentences_large.jsonl")
    )
    clean_corpus_file(
        Path("datasets/corpus/sasak_sentences_10k.csv"),
        Path("datasets/corpus/sasak_sentences_10k.jsonl")
    )
