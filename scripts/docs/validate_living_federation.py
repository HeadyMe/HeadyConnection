#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "web/living_federation/data/manifest.json"
LEGACY_MANIFEST = ROOT / "web/living_federation/data/patents.json"

REQUIRED_FIELDS = {"number", "title", "status", "summary", "integration", "tags"}


def main() -> int:
    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            print("Manifest must be an object with snapshot and patents")
            return 1
        if "snapshot" not in data or "patents" not in data:
            print("Manifest missing snapshot or patents")
            return 1
        snapshot = data.get("snapshot", {})
        for key in ("version", "generated_at", "source", "schema_version", "manifest_id"):
            if key not in snapshot:
                print(f"Snapshot missing {key}")
                return 1
        entries = data.get("patents", [])
    elif LEGACY_MANIFEST.exists():
        entries = json.loads(LEGACY_MANIFEST.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            print("Legacy manifest must be a list of patent entries")
            return 1
    else:
        print("Missing patents manifest:", MANIFEST)
        return 1

    for idx, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            print(f"Entry {idx} is not an object")
            return 1
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            print(f"Entry {idx} missing fields: {', '.join(sorted(missing))}")
            return 1
        if not isinstance(entry.get("tags"), list):
            print(f"Entry {idx} tags must be a list")
            return 1

    print("Living Federation manifest validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
