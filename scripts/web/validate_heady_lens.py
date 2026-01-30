#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = ROOT / "web" / "heady_lens"
REQUIRED_FILES = [
    "index.html",
    "main.js",
    "style.css",
    "README.md",
    "data/bodyParts.json",
    "js/modelLoader.js",
    "js/interaction.js",
    "js/overlay.js",
    "js/dataStore.js",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (DEMO_ROOT / path).exists()]
    if missing:
        print("Missing HeadyLens demo files:")
        for path in missing:
            print(f"- {path}")
        return 1

    data_path = DEMO_ROOT / "data/bodyParts.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("bodyParts.json must be a JSON object keyed by body part")
        return 1

    required_parts = {
        "heart",
        "brain",
        "left_arm",
        "right_arm",
        "lungs",
        "eyes",
        "heady_make",
        "heady_field",
        "heady_legacy",
    }
    missing_parts = required_parts - set(data.keys())
    if missing_parts:
        print(f"Missing required body parts: {', '.join(sorted(missing_parts))}")
        return 1

    for key, entry in data.items():
        for field in ("name", "description", "logic", "ip"):
            if field not in entry or not str(entry[field]).strip():
                print(f"Missing field '{field}' for body part: {key}")
                return 1
        if "assigned to HeadySystems Inc." not in entry["ip"]:
            print(f"IP entry for {key} must include assignment to HeadySystems Inc.")
            return 1

    print("HeadyLens demo validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
