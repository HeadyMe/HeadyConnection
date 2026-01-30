#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = ROOT / "governance.lock.json"
REQUIRED_FIELDS = {"governance_repo", "version", "install_method", "release_asset", "notes"}


def main() -> int:
    if not LOCK_PATH.exists():
        print("governance.lock.json is missing")
        return 1

    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("governance.lock.json must be a JSON object")
        return 1

    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        print(f"Missing fields in governance.lock.json: {', '.join(sorted(missing))}")
        return 1

    if not str(data["governance_repo"]).startswith("https://"):
        print("governance_repo must be an https URL")
        return 1

    if not str(data["release_asset"]).endswith(".tar.gz"):
        print("release_asset should be a .tar.gz asset")
        return 1

    print("Governance lock validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
