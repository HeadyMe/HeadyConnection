from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class CriminogenicFactor:
    name: str
    weight: float
    description: str


DEFAULT_FACTORS: List[CriminogenicFactor] = [
    CriminogenicFactor("prior_offenses", 0.25, "Number and severity of prior offenses."),
    CriminogenicFactor("institutional_behavior", 0.2, "Institutional conduct over time."),
    CriminogenicFactor("program_participation", 0.15, "Participation in rehabilitation programs."),
    CriminogenicFactor("support_network", 0.2, "Availability of stable community support."),
    CriminogenicFactor("employment_readiness", 0.2, "Skills and readiness for employment."),
]


def calculate_risk_score(inputs: Dict[str, float]) -> float:
    score = 0.0
    for factor in DEFAULT_FACTORS:
        score += factor.weight * inputs.get(factor.name, 0.0)
    return round(score, 3)
