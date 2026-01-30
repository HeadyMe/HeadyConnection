from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class HeadyReflectRecord:
    vertical: str
    intent: str
    usage_units: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    policy_version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vertical": self.vertical,
            "intent": self.intent,
            "usage_units": self.usage_units,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "policy_version": self.policy_version,
        }
