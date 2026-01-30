#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "web/genesis_dashboard/data/manifest.json"

REQUIRED_TOP = {"snapshot", "status", "kaizen", "signals"}
REQUIRED_SNAPSHOT = {"version", "generated_at", "source"}
REQUIRED_ITEM = {"title", "summary", "owner", "status"}


def main() -> int:
    if not MANIFEST.exists():
        print("Missing Genesis manifest:", MANIFEST)
        return 1

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not REQUIRED_TOP.issubset(payload.keys()):
        print("Genesis manifest missing required top-level keys")
        return 1

    snapshot = payload.get("snapshot", {})
    if not REQUIRED_SNAPSHOT.issubset(snapshot.keys()):
        print("Genesis snapshot missing required fields")
        return 1

    for section in ("kaizen", "signals"):
        entries = payload.get(section, [])
        if not isinstance(entries, list):
            print(f"Genesis {section} must be a list")
            return 1
        for idx, entry in enumerate(entries, start=1):
            if not REQUIRED_ITEM.issubset(entry.keys()):
                print(f"Genesis {section} entry {idx} missing required fields")
                return 1

    print("Genesis dashboard manifest validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
