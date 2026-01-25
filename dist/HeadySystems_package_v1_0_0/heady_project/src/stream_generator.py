#!/usr/bin/env python3
import time
import random
import datetime
import json
import sys
import os

# Add current dir to path to find dependencies
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from compute_throttle import UserRequest, TaskIntent
except ImportError:
    # Fallback mock if running standalone without context
    from enum import Enum
    from dataclasses import dataclass
    class TaskIntent(Enum):
        STANDARD_WEB = "web"
    @dataclass
    class UserRequest:
        user_id: str
        intent: TaskIntent
        is_sovereign_tier: bool
        urgency_score: float

def generate_stream(duration=5, interval=0.5):
    print(f"--- Starting Test Data Stream (Duration: {duration}s) ---", flush=True)
    start_time = time.time()
    users = ["admin", "dev_01", "sovereign_user", "guest_bot", "miner_node"]

    while (time.time() - start_time) < duration:
        req = UserRequest(
            user_id=random.choice(users),
            intent=random.choice(list(TaskIntent)),
            is_sovereign_tier=random.choice([True, False]),
            urgency_score=round(random.random(), 2)
        )

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "stream_generator",
            "event": "synthetic_request",
            "payload": {
                "user": req.user_id,
                "intent": req.intent.name,
                "tier": "Sovereign" if req.is_sovereign_tier else "Standard"
            }
        }
        print(json.dumps(log_entry), flush=True)
        time.sleep(interval)

if __name__ == "__main__":
    generate_stream()
