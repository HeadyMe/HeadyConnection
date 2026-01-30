from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class SafetyFilter:
    prohibited_terms: List[str] = field(
        default_factory=lambda: [
            "violence",
            "bullying",
            "self-harm",
            "weapons",
            "adult-content",
        ]
    )

    def is_allowed(self, text: str) -> bool:
        lowered = text.lower()
        return not any(term in lowered for term in self.prohibited_terms)
