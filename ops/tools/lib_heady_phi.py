from __future__ import annotations

import math
import random
from dataclasses import dataclass

PHI = (1 + math.sqrt(5)) / 2


@dataclass(frozen=True)
class PhiResult:
    value: float
    jittered: float


def backoff(attempt: int, base_delay: float = 1.0) -> PhiResult:
    delay = base_delay * (PHI ** max(0, attempt))
    jittered = delay + random.uniform(0.0, delay / PHI)
    return PhiResult(value=round(delay, 3), jittered=round(jittered, 3))


def scale_up(current_nodes: int) -> int:
    return max(1, math.ceil(current_nodes * PHI))


def decay_envelope(initial_value: float, time_step: int) -> float:
    return round(initial_value / (PHI ** max(0, time_step)), 6)
