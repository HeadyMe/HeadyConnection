#!/usr/bin/env python3
from enum import Enum
from dataclasses import dataclass
import random

class TaskIntent(Enum):
    CRITICAL_SAFETY = "safety_override"
    REALTIME_AUDIO = "audio_symphony"
    RENDER_BATCH = "video_render"
    STANDARD_WEB = "web_request"
    BACKGROUND_MINING = "pops_mining"

@dataclass
class UserRequest:
    user_id: str
    intent: TaskIntent
    is_sovereign_tier: bool = False
    urgency_score: float = 1.0

class HeadyComputeThrottle:
    def calculate_allocation(self, req):
        return {
            "cpu_cores": random.randint(1, 16),
            "ram_gb": random.randint(4, 64),
            "throttle_level": 0 if req.is_sovereign_tier else 2
        }
