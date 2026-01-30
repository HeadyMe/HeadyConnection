#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "heady_iterations"
REQUIRED = ("it1", "it2", "it3", "it4")


def main() -> int:
    if not OUTPUT_DIR.exists():
        print("Missing heady_iterations directory")
        return 1

    for name in REQUIRED:
        manifest = OUTPUT_DIR / name / "manifest.json"
        if not manifest.exists():
            print(f"Missing manifest: {manifest}")
            return 1
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if payload.get("iteration") != int(name[-1]):
            print(f"Manifest iteration mismatch for {name}")
            return 1
        if "schema_version" not in payload:
            print(f"Manifest schema_version missing for {name}")
            return 1
        if "stage_name" not in payload:
            print(f"Manifest stage_name missing for {name}")
            return 1

    print("Heady iteration manifests validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
