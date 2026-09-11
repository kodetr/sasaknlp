"""Loader utility for SasakLex entries from JSON and CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List, Union

from sasaknlp.core.types import LexiconEntry


class LexiconLoader:
    """Loads and serializes LexiconEntry objects from various data sources."""

    @staticmethod
    def load_from_json(path: Union[str, Path]) -> List[LexiconEntry]:
        """Load lexicon entries from a JSON file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Lexicon file not found at: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if not isinstance(raw_data, list):
            raise ValueError("Lexicon JSON must contain a top-level list of entries.")

        return [LexiconEntry.from_dict(item) for item in raw_data]

    @staticmethod
    def load_from_csv(path: Union[str, Path]) -> List[LexiconEntry]:
        """Load lexicon entries from a CSV file.

        Expected CSV columns:
        word,lemma,pos,meaning_id,dialect,source,frequency,prefix,infix,suffix
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Lexicon file not found at: {file_path}")

        entries: List[LexiconEntry] = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                entry_id = row.get("id") or f"CSV{idx:05d}"
                entry = LexiconEntry(
                    id=entry_id,
                    word=row.get("word", "").strip(),
                    lemma=row.get("lemma", row.get("word", "")).strip(),
                    pos=row.get("pos", "UNKNOWN").strip(),
                    meaning_id=row.get("meaning_id", "").strip(),
                    dialect=row.get("dialect", "general").strip(),
                    morphology={
                        "prefix": row.get("prefix") or None,
                        "infix": row.get("infix") or None,
                        "suffix": row.get("suffix") or None,
                    },
                    source=row.get("source", "csv_import").strip(),
                    frequency=int(row.get("frequency", 0)),
                )
                entries.append(entry)
        return entries

    @staticmethod
    def save_to_json(entries: List[LexiconEntry], path: Union[str, Path]) -> None:
        """Serialize a list of LexiconEntry objects to a formatted JSON file."""
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [e.to_dict() for e in entries]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
