#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "crypto" / "pops_oracle" / "schema.json"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_pops_oracle.py path/to/payload.json")
        return 1

    payload_path = Path(sys.argv[1])
    if not payload_path.exists():
        print(f"Payload not found: {payload_path}")
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data = json.loads(payload_path.read_text(encoding="utf-8"))

    required = set(schema.get("required", []))
    missing = required - set(data.keys())
    if missing:
        print(f"Missing required fields: {', '.join(sorted(missing))}")
        return 1

    metrics = data.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        print("metrics must be a non-empty object")
        return 1

    signature = data.get("signature")
    if not isinstance(signature, str) or len(signature) < 16:
        print("signature must be a non-empty string (min length 16)")
        return 1

    print("PoPS Oracle payload validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
