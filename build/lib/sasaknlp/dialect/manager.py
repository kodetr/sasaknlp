"""Dialect manager providing dialect taxonomy and metadata for Bahasa Sasak."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

DEFAULT_DIALECT_RULES = Path(__file__).parent / "rules" / "dialect_rules.json"


class DialectManager:
    """Manages dialect registry, dialect-specific marker lexicons, and regional rules."""

    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        self.config_path = Path(config_path or DEFAULT_DIALECT_RULES)
        self._dialects: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        """Load dialect definitions from JSON file."""
        if not self.config_path.exists():
            # Fallback minimum baseline
            self._dialects = {
                "general": {"name": "General Sasak", "markers": []},
                "selaparang": {"name": "Selaparang (Menu-Meni)", "markers": []},
            }
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._dialects = data.get("dialects", {})

    def get_supported_dialects(self) -> List[str]:
        """Return list of supported dialect code identifiers."""
        return list(self._dialects.keys())

    def is_valid_dialect(self, dialect: str) -> bool:
        """Check if dialect code is recognized."""
        return dialect.lower().strip() in self._dialects or dialect.lower().strip() == "auto"

    def get_dialect_info(self, dialect: str) -> Optional[Dict[str, Any]]:
        """Retrieve detailed metadata for a specific dialect."""
        return self._dialects.get(dialect.lower().strip())

    def get_markers(self, dialect: str) -> Set[str]:
        """Return set of diagnostic lexical marker words for a dialect."""
        info = self.get_dialect_info(dialect)
        if not info:
            return set()
        return set(m.lower().strip() for m in info.get("markers", []))

    def register_dialect(
        self, dialect_code: str, name: str, markers: List[str], description: str = ""
    ) -> None:
        """Dynamically register a new dialect or update existing configuration."""
        self._dialects[dialect_code.lower().strip()] = {
            "name": name,
            "description": description,
            "markers": markers,
        }
