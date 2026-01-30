from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from governance import HeadyReflectRecord


class TaskIntent(str, Enum):
    REALTIME_AUDIO = "REALTIME_AUDIO"
    EPHEMERAL_PROCESSING = "EPHEMERAL_PROCESSING"
    BACKGROUND_MINING = "BACKGROUND_MINING"


@dataclass
class ComputeThrottle:
    per_intent_limit: Dict[TaskIntent, float] = field(
        default_factory=lambda: {
            TaskIntent.REALTIME_AUDIO: 150.0,
            TaskIntent.EPHEMERAL_PROCESSING: 200.0,
            TaskIntent.BACKGROUND_MINING: 500.0,
        }
    )
    usage_by_vertical: Dict[str, Dict[TaskIntent, float]] = field(default_factory=dict)

    def request_intent(self, vertical: str, intent: TaskIntent, units: float, metadata: Dict[str, Any]) -> HeadyReflectRecord:
        if units <= 0:
            raise ValueError("Usage units must be positive.")
        limit = self.per_intent_limit.get(intent, 0.0)
        vertical_usage = self.usage_by_vertical.setdefault(vertical, {})
        current = vertical_usage.get(intent, 0.0)
        if current + units > limit:
            raise ValueError(f"Usage limit exceeded for {vertical} on {intent}: {current + units} > {limit}")
        vertical_usage[intent] = current + units
        return HeadyReflectRecord(
            vertical=vertical,
            intent=intent.value,
            usage_units=units,
            metadata=metadata,
        )
