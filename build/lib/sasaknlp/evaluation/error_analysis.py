"""Error analysis module categorizing stemming and morphological deviations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from sasaknlp.core.types import ErrorCategory
from sasaknlp.lexicon.manager import SasakLexManager


class ErrorAnalyzer:
    """Classifies prediction discrepancies into linguistic error taxonomy:

    - Correct: Exact match with ground truth lemma.
    - Overstemming: Prediction is an overly stripped subpart of the true lemma.
    - Understemming: Prediction retains unstripped affixes containing the true lemma.
    - Incorrect Lemma: Prediction matches neither prefix nor suffix relation.
    - OOV Error: The ground truth word/lemma is missing from the lexicon.
    - Dialect Error: Mismatch caused by dialectal variation or marker divergence.
    """

    def __init__(self, lexicon_manager: Optional[SasakLexManager] = None) -> None:
        self.lexicon = lexicon_manager or SasakLexManager()

    def classify_error(
        self,
        surface: str,
        predicted_lemma: str,
        gold_lemma: str,
        dialect: str = "general",
    ) -> ErrorCategory:
        """Classify the error category for an individual prediction."""
        p = predicted_lemma.lower().strip()
        g = gold_lemma.lower().strip()
        s = surface.lower().strip()

        # 1. Correct Match
        if p == g:
            return ErrorCategory.CORRECT

        # 2. Check if gold lemma is Out-Of-Vocabulary
        if not self.lexicon.exists(g):
            return ErrorCategory.OOV_ERROR

        # 3. Dialect Error: check if word or lemma is dialect specific
        entry = self.lexicon.lookup(g)
        if entry and entry.dialect != "general" and entry.dialect != dialect.lower().strip():
            return ErrorCategory.DIALECT_ERROR

        # 4. Overstemming: predicted lemma is shorter than gold lemma and is a substring
        if len(p) < len(g) and p in g:
            return ErrorCategory.OVERSTEMMING

        # 5. Understemming: predicted lemma is longer than gold lemma and contains gold lemma
        if len(p) > len(g) and g in p:
            return ErrorCategory.UNDERSTEMMING

        # 6. Otherwise: completely incorrect lemma
        return ErrorCategory.INCORRECT_LEMMA

    def analyze_batch(
        self,
        surfaces: List[str],
        predictions: List[str],
        ground_truth: List[str],
        dialects: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Analyze an entire batch of predictions and summarize error distributions."""
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have identical lengths.")

        dialects_list = dialects or ["general"] * len(predictions)
        surfaces_list = surfaces if surfaces else predictions

        error_counts: Dict[str, int] = {cat.value: 0 for cat in ErrorCategory}
        detailed_samples: List[Dict[str, Any]] = []

        for s, p, g, d in zip(surfaces_list, predictions, ground_truth, dialects_list):
            cat = self.classify_error(surface=s, predicted_lemma=p, gold_lemma=g, dialect=d)
            error_counts[cat.value] += 1

            if cat != ErrorCategory.CORRECT:
                detailed_samples.append({
                    "surface": s,
                    "predicted": p,
                    "ground_truth": g,
                    "dialect": d,
                    "error_category": cat.value,
                })

        total = len(ground_truth)
        distribution = {
            cat_name: {
                "count": count,
                "percentage": round((count / total) * 100, 2) if total > 0 else 0.0,
            }
            for cat_name, count in error_counts.items()
        }

        return {
            "total_samples": total,
            "error_distribution": distribution,
            "error_samples": detailed_samples,
        }
