from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class StaticInmateRecord:
    inmate_id: str
    sentencing_summary: str
    custody_level: str
    last_review_date: datetime


@dataclass
class DynamicBehaviorLog:
    inmate_id: str
    observed_at: datetime
    narrative: str
    officer_id: str


@dataclass
class InmateManagementSchema:
    static_records: List[StaticInmateRecord] = field(default_factory=list)
    dynamic_logs: List[DynamicBehaviorLog] = field(default_factory=list)
