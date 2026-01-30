from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional


@dataclass
class MemoryTrigger:
    trigger_id: str
    prompt_type: str
    prompt_value: str
    last_triggered_at: Optional[datetime] = None


class StimulusLoop:
    def __init__(self, reengagement_hours: int = 48) -> None:
        self._triggers: Dict[str, MemoryTrigger] = {}
        self._last_activity_at: datetime = datetime.utcnow()
        self._reengagement_delta = timedelta(hours=reengagement_hours)

    def record_activity(self) -> None:
        self._last_activity_at = datetime.utcnow()

    def add_trigger(self, trigger: MemoryTrigger) -> None:
        self._triggers[trigger.trigger_id] = trigger

    def should_reengage(self) -> bool:
        return datetime.utcnow() - self._last_activity_at > self._reengagement_delta

    async def scheduler(self, callback: Callable[[MemoryTrigger], None]) -> None:
        while True:
            await asyncio.sleep(60)
            if not self.should_reengage():
                continue
            for trigger in self._triggers.values():
                trigger.last_triggered_at = datetime.utcnow()
                callback(trigger)
            self.record_activity()
