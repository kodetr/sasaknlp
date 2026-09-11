"""
Script to harvest and parse the official Kamus Bahasa Sasak
from Balai Bahasa Provinsi NTB (Kamus Terpadu Sasambo).
URL: https://kamusterpadusasambo.kemendikdasmen.go.id/
"""

import urllib.request
import ssl
import json
import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def harvest_kamus_balai_bahasa():
    ctx = ssl._create_unverified_context()
    # Search with all vowels to cover Austronesian phonology exhaustively
    search_queries = ['a', 'e', 'i', 'u', 'o']
    all_entries = {}
    
    print("=== Harvesting Kamus Terpadu Sasambo (Balai Bahasa Provinsi NTB) ===")
    
    for query in search_queries:
        url = f"https://kamusterpadusasambo.kemendikdasmen.go.id/pencarian/kata?query={query}"
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SasakNLP/1.0"}
        )
        try:
            print(f"Fetching query '{query}' from {url}...")
            with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
                html = r.read().decode('utf-8', errors='ignore')
            
            soup = BeautifulSoup(html, 'html.parser')
            boxes = soup.find_all('div', class_='box_detail')
            print(f"  Received {len(boxes)} boxes for query '{query}'")
            
            for b in boxes:
                title_elem = b.find('strong')
                if not title_elem:
                    continue
                title = clean_text(title_elem.text)
                if not title:
                    continue
                
                dl = b.find('dl')
                if not dl:
                    continue
                
                dts = [clean_text(dt.text) for dt in dl.find_all('dt')]
                dds = [clean_text(dd.text) for dd in dl.find_all('dd')]
                info = dict(zip(dts, dds))
                
                bahasa = info.get('Bahasa', '').strip().lower()
                if bahasa != 'sasak':
                    continue
                
                # If entry already exists, merge info if needed
                if title not in all_entries:
                    # Clean lemma: remove alternative forms like "; ajar" or ", ajarang"
                    first_part = title.split(';')[0].split(',')[0].strip()
                    # Remove parenthesized affixes like "pe(r,l)ajahan" -> "pelajahan"
                    clean_lemma = re.sub(r'\([^)]*\)', '', first_part).strip()
                    
                    all_entries[title] = {
                        "word": title,
                        "lemma": clean_lemma.lower(),
                        "pos": info.get("Kelas Kata", "").strip(),
                        "dialect": info.get("Dialek", "").strip() or "Sasak Umum",
                        "meaning_id": info.get("Makna 1", "").strip(),
                        "meaning_2": info.get("Makna 2", "").strip(),
                        "example": info.get("Contoh 1", "").strip(),
                        "source": "Balai Bahasa Provinsi NTB (Kamus Terpadu Sasambo)"
                    }
        except Exception as e:
            print(f"Error fetching query '{query}': {e}")
            
    print(f"\nTotal unique Sasak entries harvested: {len(all_entries)}")
    
    # Save to JSON
    output_dir = Path("datasets/sasaklex")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "kamus_balai_bahasa_ntb.json"
    csv_path = output_dir / "kamus_balai_bahasa_ntb.csv"
    
    entries_list = list(all_entries.values())
    entries_list.sort(key=lambda x: x["word"].lower())
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries_list, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON to: {json_path} ({len(entries_list)} entries)")
    
    # Save to CSV
    fieldnames = ["word", "lemma", "pos", "dialect", "meaning_id", "meaning_2", "example", "source"]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries_list)
    print(f"Saved CSV to: {csv_path} ({len(entries_list)} rows)")
    
    return entries_list

if __name__ == "__main__":
    harvest_kamus_balai_bahasa()
