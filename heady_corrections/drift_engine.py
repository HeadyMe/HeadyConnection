from __future__ import annotations

import math
from collections import Counter, deque
from dataclasses import dataclass
from typing import Deque, Iterable


@dataclass
class RiskEvaluation:
    variance_score: float
    risk_alert: bool


def _tokenize(text: str) -> Counter[str]:
    tokens = [token.lower() for token in text.split() if token.strip()]
    return Counter(tokens)


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    all_keys = set(left) | set(right)
    if not all_keys:
        return 1.0
    dot = sum(left[key] * right[key] for key in all_keys)
    left_norm = math.sqrt(sum(value ** 2 for value in left.values()))
    right_norm = math.sqrt(sum(value ** 2 for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


class SemanticDrift:
    def __init__(self, max_entries: int = 30) -> None:
        self._baseline: Deque[Counter[str]] = deque(maxlen=max_entries)

    def seed(self, narratives: Iterable[str]) -> None:
        for narrative in narratives:
            self._baseline.append(_tokenize(narrative))

    def evaluate_risk(self, narrative: str, threshold: float = 7.0) -> RiskEvaluation:
        vector = _tokenize(narrative)
        if not self._baseline:
            self._baseline.append(vector)
            return RiskEvaluation(variance_score=0.0, risk_alert=False)

        similarities = [_cosine_similarity(vector, baseline) for baseline in self._baseline]
        avg_similarity = sum(similarities) / len(similarities)
        variance = max(0.0, 1.0 - avg_similarity)
        variance_score = round(min(10.0, variance * 10.0), 2)
        risk_alert = variance_score > threshold
        self._baseline.append(vector)
        return RiskEvaluation(variance_score=variance_score, risk_alert=risk_alert)
