"""Dialect detection framework and baseline heuristic detector for Bahasa Sasak."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from sasaknlp.dialect.manager import DialectManager


class DialectDetector:
    """Baseline heuristic dialect detector using diagnostic lexical markers.

    Note on Research Validity:
    Per SasakNLP research guidelines, dialect classification in low-resource
    languages requires careful reporting. This detector provides a transparent
    lexical marker matching baseline. When insufficient diagnostic markers
    are found, it defaults to 'general' with an appropriately low confidence score.
    """

    def __init__(self, dialect_manager: Optional[DialectManager] = None) -> None:
        self.manager = dialect_manager or DialectManager()

    def detect(self, tokens: List[str]) -> Tuple[str, float]:
        """Detect the most probable dialect for a list of tokens.

        Args:
            tokens: List of normalized word tokens.

        Returns:
            Tuple of (detected_dialect_code, confidence_score [0.0, 1.0]).
        """
        if not tokens:
            return "general", 0.0

        token_set = {t.lower().strip() for t in tokens if t}
        scores: Dict[str, int] = {}

        # Count marker hits per dialect (excluding 'general')
        for dialect in self.manager.get_supported_dialects():
            if dialect == "general":
                continue
            markers = self.manager.get_markers(dialect)
            matches = token_set.intersection(markers)
            scores[dialect] = len(matches)

        best_dialect = "general"
        best_count = 0
        total_markers_matched = 0

        for dialect, count in scores.items():
            total_markers_matched += count
            if count > best_count:
                best_count = count
                best_dialect = dialect

        if best_count == 0:
            # No dialect-specific shibboleths matched; return general baseline
            return "general", 0.50

        # Calibrate confidence based on matched markers and sample length
        # e.g., 1 marker = 0.65, 2 markers = 0.80, 3+ = 0.90
        confidence = min(0.95, 0.50 + (best_count * 0.15))

        return best_dialect, round(confidence, 4)

    def get_dialect_distribution(self, tokens: List[str]) -> Dict[str, float]:
        """Return proportion of matched markers across dialects."""
        if not tokens:
            return {"general": 1.0}

        token_set = {t.lower().strip() for t in tokens}
        counts: Dict[str, int] = {}
        total = 0

        for dialect in self.manager.get_supported_dialects():
            markers = self.manager.get_markers(dialect)
            c = len(token_set.intersection(markers))
            counts[dialect] = c
            total += c

        if total == 0:
            return {"general": 1.0}

        return {d: round(c / total, 4) for d, c in counts.items() if c > 0}
