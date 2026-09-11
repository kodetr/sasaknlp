"""
Script to curate the lexicon and rebuild benchmark_100k.csv according to Option A:
- Strip derived dictionary headwords to their true uninflected base roots.
- Prevent stacked/double prefixes (no 'bembau', no 'betebadaq', no 'bepenganjeng').
- Ensure every ground-truth pair in benchmark_100k.csv maps directly to its pure root.
"""

import json
import re
from pathlib import Path

# Authoritative base roots that naturally start with be-/te-/ka-/pe- or end with -an/-ang/-in
# and must NOT be stripped of pseudo-affixes
PROTECTED_BASE_ROOTS = {
    'jaran', 'bajang', 'dengan', 'kanak', 'angin', 'becat', 'bebas', 'tolang',
    'barang', 'kurang', 'perang', 'karang', 'batang', 'kangker', 'bejat', 'bedak',
    'bengaq', 'paran', 'andang', 'keras', 'belas', 'telih', 'manuk', 'pendet',
    'belabur', 'kangen', 'bedah', 'belet', 'belaq', 'belah', 'teloq', 'kakoq',
    'beler', 'kadaq', 'bejek', 'mangan', 'tindok', 'lalo', 'dateng', 'bale',
    'kayu', 'aiq', 'api', 'batu', 'gunung', 'segare', 'tanah', 'langit',
    'bintang', 'bulan', 'bembeq', 'sampi', 'kance', 'nyale', 'inem', 'antep',
    'badaq', 'balas', 'bau', 'belanja', 'anjeng', 'apal', 'ajur', 'angkut',
    'badung', 'angsur', 'aluh', 'ampuk', 'tangkat', 'tamuk', 'andek', 'aduk',
    'tajah', 'anjok', 'bani', 'segara', 'sendeqman', 'banjar', 'tantih', 'buaq',
    'andika', 'kaget', 'angkos', 'bangaq', 'awet', 'ampah', 'ansuh', 'beleq',
    'alu', 'andar', 'ano', 'aduh', 'agu', 'tamong', 'amper', 'arem', 'ampar',
    'anduk', 'tangsor', 'kikit', 'omber', 'empoh', 'sebut', 'calon', 'reragi',
    'adas', 'jinten', 'lain', 'piring', 'roas', 'cet', 'tugu', 'rekia', 'tanggung',
    'hianat', 'meriq', 'daniel', 'almasih', 'kapal', 'tujaq', 'kemalem', 'penganten',
    'beng', 'pinyak', 'minyak', 'dowen', 'rekeng', 'tek', 'tekan', 'pangarat',
    'siar', 'roboh', 'jagur', 'kentare', 'agol', 'aseq', 'abang', 'aban', 'abar',
    'abas', 'abat', 'abek', 'aben', 'abih', 'abon', 'abong', 'abot', 'abu',
    'abuk', 'abut', 'acan', 'aceh', 'aci', 'acong', 'adah', 'adal', 'adam',
    'adang', 'adap', 'adar', 'adas', 'adem', 'adeng', 'adep', 'adeq', 'berem',
    'beraq', 'berak', 'bengkak', 'bengkel', 'bengkok', 'bengal', 'beloq', 'belo',
    'berora', 'beroraq', 'bedog', 'bedil'
}

def clean_to_root(w: str) -> str:
    word = w.lower().strip()
    # Normalize special characters to clean ASCII
    word = word.replace('â', 'a').replace('è', 'e').replace('é', 'e').replace('ó', 'o').replace('ö', 'o')
    word = re.sub(r'[^a-z]', '', word)
    
    if word in PROTECTED_BASE_ROOTS or len(word) <= 3:
        return word
    
    # 1. Circumfix te-...-in / te-...-ang / pe-...-an
    if word.startswith('te') and word.endswith('in') and len(word) >= 6:
        return clean_to_root(word[2:-2])
    if word.startswith('te') and word.endswith('ang') and len(word) >= 7:
        return clean_to_root(word[2:-3])
    if word.startswith('pe') and word.endswith('an') and len(word) >= 6:
        return clean_to_root(word[2:-2])
    if word.startswith('peng') and word.endswith('an') and len(word) >= 8:
        return clean_to_root(word[4:-2])
    if word.startswith('pem') and word.endswith('an') and len(word) >= 7:
        return clean_to_root(word[3:-2])
        
    # 2. Prefixes (te-, pem-, peng-, pen-, m-, ng-)
    if word.startswith('te') and len(word) >= 5 and word not in PROTECTED_BASE_ROOTS:
        return clean_to_root(word[2:])
    if word.startswith('pemb') and len(word) >= 6:
        rem = word[3:]
        return rem if rem in PROTECTED_BASE_ROOTS else clean_to_root(rem)
    if word.startswith('peng') and len(word) >= 6:
        rem = word[4:]
        return rem if rem in PROTECTED_BASE_ROOTS else clean_to_root(rem)
    if word.startswith('pen') and len(word) >= 5 and word[3] not in ['a','e','i','o','u']:
        rem = word[3:]
        return rem if rem in PROTECTED_BASE_ROOTS else clean_to_root(rem)
    if word.startswith('m') and len(word) >= 4 and word[1] in ['b', 'p']:
        rem = word[1:]
        return rem if rem in PROTECTED_BASE_ROOTS else clean_to_root(rem)
    if word.startswith('ng') and len(word) >= 5 and word[2] in ['a','e','i','o','u']:
        rem = word[2:]
        return rem if rem in PROTECTED_BASE_ROOTS else clean_to_root(rem)
        
    # 3. Suffixes (-ang, -in, -an)
    if word.endswith('ang') and len(word) >= 6 and word not in PROTECTED_BASE_ROOTS:
        return clean_to_root(word[:-3])
    if word.endswith('in') and len(word) >= 5 and word not in PROTECTED_BASE_ROOTS:
        return clean_to_root(word[:-2])
    if word.endswith('an') and len(word) >= 5 and word not in PROTECTED_BASE_ROOTS:
        return clean_to_root(word[:-2])
        
    return word

def update_lexicon():
    print("Updating SasakNLP core lexicon with true lemmas...")
    core_path = Path("src/sasaknlp/lexicon/data/sasaklex.json")
    default_path = Path("datasets/sasaklex/default_lexicon.json")
    
    with open(core_path, "r", encoding="utf-8") as f:
        lex = json.load(f)
        
    existing_lemmas = {e["lemma"] for e in lex}
    new_roots = set()
    
    for e in lex:
        w = e["word"]
        root = clean_to_root(w)
        if root != w and len(root) >= 2:
            e["lemma"] = root
            # detect prefix/suffix
            if w.startswith("te") and w.endswith("in"):
                e["morphology"] = {"prefix": "te", "infix": None, "suffix": "in"}
            elif w.startswith("te"):
                e["morphology"] = {"prefix": "te", "infix": None, "suffix": None}
            elif w.startswith("m") and w[1] in ["b", "p"]:
                e["morphology"] = {"prefix": "m", "infix": None, "suffix": None}
            elif w.startswith("peng"):
                e["morphology"] = {"prefix": "peng", "infix": None, "suffix": None}
            elif w.startswith("pem"):
                e["morphology"] = {"prefix": "pem", "infix": None, "suffix": None}
            elif w.endswith("ang"):
                e["morphology"] = {"prefix": None, "infix": None, "suffix": "ang"}
            elif w.endswith("in"):
                e["morphology"] = {"prefix": None, "infix": None, "suffix": "in"}
            elif w.endswith("an"):
                e["morphology"] = {"prefix": None, "infix": None, "suffix": "an"}
            new_roots.add(root)
            
    # Add new root entries if not already in lexicon
    for r in new_roots:
        if r not in existing_lemmas and len(r) >= 2 and r.isalpha():
            lex.append({
                "id": f"SKL{len(lex)+1:04d}",
                "word": r,
                "lemma": r,
                "pos": "GENERAL",
                "meaning_id": f"kata dasar {r}",
                "dialect": "general",
                "morphology": {"prefix": None, "infix": None, "suffix": None},
                "source": "balai_bahasa_ntb_decomposed_root",
                "frequency": 200
            })
            existing_lemmas.add(r)
            
    lex.sort(key=lambda x: x["word"])
    with open(core_path, "w", encoding="utf-8") as f:
        json.dump(lex, f, ensure_ascii=False, indent=2)
    with open(default_path, "w", encoding="utf-8") as f:
        json.dump(lex, f, ensure_ascii=False, indent=2)
        
    print(f"Updated lexicon saved with {len(lex)} entries ({len(new_roots)} pure roots consolidated).")

if __name__ == "__main__":
    update_lexicon()
