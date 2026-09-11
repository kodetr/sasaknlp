"""Candidate ranking engine for morphological root candidates."""

from __future__ import annotations

import math
from typing import List, Optional

from sasaknlp.core.config import RankingWeights
from sasaknlp.core.types import MorphologicalCandidate, ValidationStatus


class CandidateRanker:
    """Ranks morphological candidates using a multi-criteria scoring function.

    Formula:
        Score = w_lex * S_lex + w_morph * S_morph + w_conf * S_conf + w_freq * S_freq + w_dial * S_dial
    """

    def __init__(self, weights: Optional[RankingWeights] = None) -> None:
        self.weights = weights or RankingWeights()
        self.weights.validate()

    def score_candidate(
        self, candidate: MorphologicalCandidate, target_dialect: str = "general"
    ) -> float:
        """Calculate weighted score for an individual candidate."""
        # 1. Lexicon match score
        if candidate.validation_status == ValidationStatus.EXACT_MATCH:
            s_lex = 1.0
        elif candidate.validation_status == ValidationStatus.PARTIAL_MATCH:
            s_lex = 0.5
        elif candidate.validation_status == ValidationStatus.OOV:
            s_lex = 0.2
        else:
            s_lex = 0.0

        # 2. Morphological validity score
        root = candidate.lemma_candidate
        root_len = len(root)
        if root_len < 3:
            s_morph = 0.3
        elif 3 <= root_len <= 8:
            s_morph = 1.0
        else:
            s_morph = 0.7

        # Reward identity match if exact in lexicon
        if candidate.rule_applied == "identity":
            if candidate.validation_status == ValidationStatus.EXACT_MATCH:
                s_morph = 1.0
            else:
                # Identity without lexicon match has lower morphological validity
                s_morph = 0.4

        # 3. Rule confidence score (provided by the rule match)
        s_conf = max(0.0, min(1.0, candidate.score))

        # 4. Word frequency score (log-normalized)
        raw_freq = candidate.metadata.get("frequency", 0)
        s_freq = min(1.0, math.log10(raw_freq + 1) / 3.5) if raw_freq > 0 else 0.1

        # 5. Dialect compatibility score
        cand_dialect = candidate.metadata.get("dialect", "general")
        target_norm = target_dialect.lower().strip()
        if cand_dialect == "general" or target_norm in ("general", "auto"):
            s_dial = 1.0
        elif cand_dialect.lower() == target_norm:
            s_dial = 1.0
        else:
            s_dial = 0.4

        # Compute total composite score
        total_score = (
            self.weights.lexicon_match * s_lex
            + self.weights.morphological_validity * s_morph
            + self.weights.rule_confidence * s_conf
            + self.weights.frequency * s_freq
            + self.weights.dialect_compatibility * s_dial
        )

        candidate.breakdown_scores = {
            "s_lex": round(s_lex, 4),
            "s_morph": round(s_morph, 4),
            "s_conf": round(s_conf, 4),
            "s_freq": round(s_freq, 4),
            "s_dial": round(s_dial, 4),
            "total": round(total_score, 4),
        }
        candidate.score = total_score
        return total_score

    def rank_all(
        self, candidates: List[MorphologicalCandidate], target_dialect: str = "general"
    ) -> List[MorphologicalCandidate]:
        """Score and sort all candidates in descending order of composite score."""
        for cand in candidates:
            self.score_candidate(cand, target_dialect=target_dialect)

        # Sort: Primary key is score descending, secondary key is exact match status, third is root length
        return sorted(
            candidates,
            key=lambda c: (
                c.score,
                1 if c.validation_status == ValidationStatus.EXACT_MATCH else 0,
                -len(c.lemma_candidate),
            ),
            reverse=True,
        )

    def rank(
        self, candidates: List[MorphologicalCandidate], target_dialect: str = "general"
    ) -> Optional[MorphologicalCandidate]:
        """Return single top-ranked candidate."""
        ranked = self.rank_all(candidates, target_dialect=target_dialect)
        return ranked[0] if ranked else None
