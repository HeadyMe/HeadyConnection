#!/usr/bin/env python3
from __future__ import annotations

import base64
import binascii
import json
import sys
from datetime import datetime
from pathlib import Path


def parse_timestamp(value: str) -> bool:
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_receipt(entry: dict, line_no: int) -> bool:
    payload = entry.get("payload")
    signature = entry.get("signature")
    public_key = entry.get("public_key")

    if not isinstance(payload, dict):
        print(f"Line {line_no}: payload must be an object")
        return False
    if not isinstance(signature, str) or not signature:
        print(f"Line {line_no}: signature must be a non-empty string")
        return False
    if not isinstance(public_key, str) or "BEGIN PUBLIC KEY" not in public_key:
        print(f"Line {line_no}: public_key must include PEM header")
        return False

    try:
        base64.b64decode(signature, validate=True)
    except (ValueError, binascii.Error):
        print(f"Line {line_no}: signature must be base64 encoded")
        return False

    required_payload_fields = ["change_id", "summary", "files", "risk", "rollback", "timestamp"]
    for field in required_payload_fields:
        if field not in payload:
            print(f"Line {line_no}: payload missing field '{field}'")
            return False

    if not isinstance(payload["files"], list) or not payload["files"]:
        print(f"Line {line_no}: payload.files must be a non-empty list")
        return False

    if not parse_timestamp(str(payload["timestamp"])):
        print(f"Line {line_no}: payload.timestamp must be an ISO-8601 timestamp")
        return False

    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_receipts.py path/to/receipts.jsonl")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Receipts file not found: {path}")
        return 1

    failures = 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"Line {line_no}: invalid JSON ({exc})")
            failures += 1
            continue
        if not validate_receipt(entry, line_no):
            failures += 1

    if failures:
        print(f"Receipt validation failed with {failures} error(s)")
        return 1

    print("Receipt validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
