#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ALLOWED_STATUSES = {"ok", "degraded", "outage", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Trust Center status feed JSON file.")
    parser.add_argument("path", help="Path to status feed JSON")
    return parser.parse_args()


def parse_timestamp(value: str) -> bool:
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if not path.exists():
        print(f"Status feed not found: {path}")
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}")
        return 1

    if not isinstance(data, dict):
        print("Status feed must be a JSON object")
        return 1

    status = data.get("status")
    summary = data.get("summary")

    if status not in ALLOWED_STATUSES:
        print(f"Invalid status: {status}. Expected one of {sorted(ALLOWED_STATUSES)}")
        return 1

    if not isinstance(summary, str) or not summary.strip():
        print("Summary is required and must be a non-empty string")
        return 1

    if len(summary) > 200:
        print("Summary must be <= 200 characters")
        return 1

    updated_at = data.get("updated_at")
    if updated_at is not None:
        if not isinstance(updated_at, str) or not parse_timestamp(updated_at):
            print("updated_at must be an ISO-8601 timestamp string")
            return 1

    components = data.get("components")
    if components is not None:
        if not isinstance(components, list) or not components:
            print("components must be a non-empty list when provided")
            return 1
        for index, component in enumerate(components):
            if not isinstance(component, dict):
                print(f"components[{index}] must be an object")
                return 1
            name = component.get("name")
            comp_status = component.get("status")
            comp_summary = component.get("summary")
            if not isinstance(name, str) or not name.strip():
                print(f"components[{index}].name must be a non-empty string")
                return 1
            if comp_status not in ALLOWED_STATUSES:
                print(f"components[{index}].status must be one of {sorted(ALLOWED_STATUSES)}")
                return 1
            if not isinstance(comp_summary, str) or not comp_summary.strip():
                print(f"components[{index}].summary must be a non-empty string")
                return 1
            comp_updated = component.get("updated_at")
            if comp_updated is not None:
                if not isinstance(comp_updated, str) or not parse_timestamp(comp_updated):
                    print(f"components[{index}].updated_at must be an ISO-8601 timestamp string")
                    return 1

    print("Status feed validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
