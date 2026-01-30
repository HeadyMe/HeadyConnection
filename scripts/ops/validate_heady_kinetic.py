#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "apps" / "heady_kinetic" / "kinetic_governance.py"


def main() -> int:
    if not APP.exists():
        print("HeadyKinetic demo script is missing.")
        return 1

    result = subprocess.run(
        [sys.executable, str(APP), "--demo"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("HeadyKinetic demo failed:")
        print(result.stderr)
        return 1

    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError as exc:
        print(f"HeadyKinetic output is not valid JSON: {exc}")
        return 1

    required = {"agent_state", "comms_state", "policy", "alerts", "alert_count", "generated_at", "proof_of_state"}
    missing = required - set(payload.keys())
    if missing:
        print(f"HeadyKinetic report missing fields: {', '.join(sorted(missing))}")
        return 1

    print("HeadyKinetic validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
