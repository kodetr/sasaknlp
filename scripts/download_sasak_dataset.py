#!/usr/bin/env python3
"""Dataset Downloader and Builder for Bahasa Sasak Corpus (10,000+ Sentences).

Aggregates authentic Sasak text data from open repositories:
1. Alkitab Mobile SABDA Bahasa Sasak (Perjanjian Baru: 27 books, 260 chapters, ~7,950 verses)
2. Wikimedia Incubator Bahasa Sasak (Wp/sas: 585 encyclopedia articles, ~4,000+ sentences)

Output:
- datasets/corpus/sasak_corpus_10k.csv
- datasets/corpus/sasak_corpus_10k.jsonl
"""

import csv
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

BOOKS_NT = [
    ("Mat", 28), ("Mrk", 16), ("Luk", 24), ("Yoh", 21), ("Kis", 28),
    ("Rom", 16), ("1Ko", 16), ("2Ko", 13), ("Gal", 6),  ("Efe", 6),
    ("Flp", 4),  ("Kol", 4),  ("1Te", 5),  ("2Te", 3),  ("1Ti", 6),
    ("2Ti", 4),  ("Tit", 3),  ("Flm", 1),  ("Ibr", 13), ("Yak", 5),
    ("1Pt", 5),  ("2Pt", 3),  ("1Yo", 5),  ("2Yo", 1),  ("3Yo", 1),
    ("Yud", 1),  ("Why", 22)
]


class SasakDatasetBuilder:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(__file__).parent.parent / "datasets" / "corpus"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.ssl_ctx = ssl._create_unverified_context()

    def fetch_url(self, url: str, retries: int = 3, delay: float = 0.5) -> Optional[str]:
        req = urllib.request.Request(url, headers={"User-Agent": "SasakNLP-Research-Toolkit/1.0"})
        for attempt in range(retries):
            try:
                time.sleep(delay)
                with urllib.request.urlopen(req, context=self.ssl_ctx, timeout=10) as resp:
                    return resp.read().decode("utf-8", errors="ignore")
            except Exception:
                time.sleep(delay * 2)
        return None

    def scrape_sabda_sasak(self, max_verses: int = 8000) -> List[Dict[str, str]]:
        """Scrape verses from alkitab.mobi/sasak."""
        records: List[Dict[str, str]] = []
        verse_pattern = re.compile(r'<p><span class="reftext"><a[^>]*>(\d+)</a></span>(.*?)</p>', re.DOTALL)
        tag_pattern = re.compile(r'<[^>]+>')

        print("[1/2] Harvesting Sasak text from SABDA Alkitab PB Sasak...")
        for book, num_chapters in BOOKS_NT:
            for ch in range(1, num_chapters + 1):
                url = f"https://alkitab.mobi/sasak/{book}/{ch}/"
                html = self.fetch_url(url, delay=0.1)
                if not html:
                    continue

                matches = verse_pattern.findall(html)
                for vnum, vtext in matches:
                    clean_text = tag_pattern.sub("", vtext).strip()
                    # Skip empty cross-reference verse pointers like '(1:2)'
                    if clean_text and not re.match(r"^\(\d+:\d+\)$", clean_text):
                        records.append({
                            "id": f"SABDA_{book}_{ch}_{vnum}",
                            "text": clean_text,
                            "source": f"alkitab_sasak_{book}_{ch}:{vnum}",
                            "type": "verse"
                        })
                        if len(records) >= max_verses:
                            return records
                print(f"  • {book} {ch}/{num_chapters} - Harvested: {len(records)} sentences", end="\r")
        print(f"\n  ✓ Completed SABDA harvesting: {len(records)} verses.")
        return records

    def scrape_wikimedia_sasak(self, target_sentences: int = 4000) -> List[Dict[str, str]]:
        """Harvest article sentences from Wikimedia Incubator Wp/sas."""
        records: List[Dict[str, str]] = []
        print("[2/2] Harvesting Wikimedia Incubator Bahasa Sasak articles (Wp/sas)...")

        api_url = (
            "https://incubator.wikimedia.org/w/api.php?action=query&generator=allpages"
            "&gapprefix=Wp/sas/&gaplimit=50&prop=extracts&explaintext=1&format=json"
        )
        current_url = api_url

        while len(records) < target_sentences:
            html = self.fetch_url(current_url, delay=0.3)
            if not html:
                break
            try:
                data = json.loads(html)
            except Exception:
                break

            pages = data.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                title = p.get("title", "").replace("Wp/sas/", "")
                extract = p.get("extract", "").strip()
                if not extract:
                    continue

                # Split sentences
                sentences = re.split(r"(?<=[.!?])\s+", extract)
                for idx, sent in enumerate(sentences, start=1):
                    clean_sent = sent.strip()
                    if len(clean_sent) > 15 and any(c.isalpha() for c in clean_sent):
                        records.append({
                            "id": f"WIKI_{title}_{idx}",
                            "text": clean_sent,
                            "source": f"wikimedia_sas_{title}",
                            "type": "encyclopedia"
                        })
                        if len(records) >= target_sentences:
                            break

            if "continue" in data:
                cont = data["continue"]
                current_url = api_url
                for k, v in cont.items():
                    current_url += f"&{k}={urllib.parse.quote(str(v))}"
            else:
                break
            print(f"  • Harvested Wikimedia sentences: {len(records)}", end="\r")

        print(f"\n  ✓ Completed Wikimedia harvesting: {len(records)} sentences.")
        return records

    def build_and_save(self, target_total: int = 10000) -> Path:
        """Aggregate and save dataset in CSV and JSONL formats."""
        records = self.scrape_sabda_sasak(max_verses=7500)
        needed = max(2500, target_total - len(records))
        wiki_records = self.scrape_wikimedia_sasak(target_sentences=needed)
        records.extend(wiki_records)

        csv_path = self.output_dir / "sasak_corpus_10k.csv"
        jsonl_path = self.output_dir / "sasak_corpus_10k.jsonl"

        # Save CSV
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "text", "source", "type"])
            writer.writeheader()
            writer.writerows(records)

        # Save JSONL
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        print(f"\nSuccessfully created Sasak 10K+ Dataset:")
        print(f"  • Total sentences: {len(records):,}")
        print(f"  • CSV:   {csv_path.resolve()}")
        print(f"  • JSONL: {jsonl_path.resolve()}")
        return csv_path


if __name__ == "__main__":
    builder = SasakDatasetBuilder()
    builder.build_and_save(target_total=10000)
