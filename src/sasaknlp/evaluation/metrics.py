"""Evaluation metrics for morphological analysis and stemming."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Sequence


def compute_accuracy(predictions: Sequence[str], ground_truth: Sequence[str]) -> float:
    """Calculate overall accuracy (proportion of exact matches)."""
    if not ground_truth:
        return 0.0
    if len(predictions) != len(ground_truth):
        raise ValueError(
            f"Length mismatch: {len(predictions)} predictions vs {len(ground_truth)} ground truth."
        )

    matches = sum(1 for p, g in zip(predictions, ground_truth) if p.strip().lower() == g.strip().lower())
    return round(matches / len(ground_truth), 4)


def compute_precision_recall_f1(
    predictions: Sequence[str], ground_truth: Sequence[str]
) -> Dict[str, float]:
    """Compute Macro and Weighted Precision, Recall, and F1-score for lemma prediction."""
    if not ground_truth:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    all_classes = set(g.strip().lower() for g in ground_truth).union(
        p.strip().lower() for p in predictions
    )

    precisions: List[float] = []
    recalls: List[float] = []
    f1s: List[float] = []
    weights: List[int] = []

    gt_counts = Counter(g.strip().lower() for g in ground_truth)
    pred_counts = Counter(p.strip().lower() for p in predictions)

    tp_counts: Counter[str] = Counter()
    for p, g in zip(predictions, ground_truth):
        p_l = p.strip().lower()
        g_l = g.strip().lower()
        if p_l == g_l:
            tp_counts[p_l] += 1

    for c in all_classes:
        tp = tp_counts[c]
        fp = pred_counts[c] - tp
        fn = gt_counts[c] - tp
        support = gt_counts[c]

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        if support > 0:
            precisions.append(prec)
            recalls.append(rec)
            f1s.append(f1)
            weights.append(support)

    total_weight = sum(weights)
    if total_weight == 0:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    macro_precision = sum(precisions) / len(precisions)
    macro_recall = sum(recalls) / len(recalls)
    macro_f1 = sum(f1s) / len(f1s)

    weighted_f1 = sum(f * w for f, w in zip(f1s, weights)) / total_weight

    return {
        "precision": round(macro_precision, 4),
        "recall": round(macro_recall, 4),
        "f1_score": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
    }
