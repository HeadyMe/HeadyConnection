#!/usr/bin/env python3
"""
HEADY GUARDIAN BOT
------------------
Simulates a GitHub App bot that listens for webhooks, validates intent via HeadyReflect,
checks resource budgets via HeadyComputeThrottle, and triggers the ConsolidatedBuilder.
"""

import os
import sys
import json
import datetime

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from heady_reflect import HeadyReflect
    from compute_throttle import HeadyComputeThrottle, UserRequest, TaskIntent
    import consolidated_builder
except ImportError as e:
    print(f"Import Error: {e}")
    # Mocks for standalone testing if needed
    class HeadyReflect:
        def validate_intent(self, i): return True
    class HeadyComputeThrottle:
        def calculate_allocation(self, r): return {"cpu_cores": 4, "ram_gb": 16, "status": "Mock Allocation"}
    class consolidated_builder:
        @staticmethod
        def execute_build(): print("Build Executed")
    class UserRequest:
        def __init__(self, user_id, intent, is_sovereign_tier):
            self.user_id = user_id
            self.intent = intent
            self.is_sovereign_tier = is_sovereign_tier
    class TaskIntent:
        RENDER_BATCH = "rb"

class HeadyGuardianBot:
    def __init__(self):
        print("ᾑ6 [INIT] HeadyGuardianBot Active. Listening for webhooks...")
        self.governance = HeadyReflect()
        self.throttle = HeadyComputeThrottle()

    def trigger_event(self, event_type, payload):
        print(f"\n὎5 [EVENT] Received {event_type}")

        # Extract intent/message
        message = payload.get("message", "Unknown Intent")
        user = payload.get("user", "system_bot")
        print(f"   User: {user} | Message: {message}")

        # 1. Governance Validation
        if not self.governance.validate_intent(message):
            print("   Ὥ1 [BLOCK] Governance check failed. Build aborted.")
            return

        # 2. Resource Check
        req = UserRequest(user_id=user, intent=TaskIntent.RENDER_BATCH, is_sovereign_tier=True)
        allocation = self.throttle.calculate_allocation(req)
        print(f"   ⚖️ [RESOURCE] Allocation: {allocation}")

        # 3. Trigger Build
        print("   Ὠ0 [ACTION] Validated. Triggering Consolidated Builder...")
        consolidated_builder.execute_build()

if __name__ == "__main__":
    # Smoke Test
    bot = HeadyGuardianBot()
    test_payload = {"user": "guardian_dev", "message": "Update Security Protocols"}
    bot.trigger_event("push", test_payload)
