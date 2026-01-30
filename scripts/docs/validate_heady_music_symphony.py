#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "heady_music_symphony"
REPOS = ("heady-music", "heady-symphony")
REQUIRED_SUBDIRS = ("app", "docs", "ops", "scripts")


def main() -> int:
    if not OUTPUT_DIR.exists():
        print("Missing output directory:", OUTPUT_DIR)
        return 1

    for repo in REPOS:
        repo_dir = OUTPUT_DIR / repo
        if not repo_dir.exists():
            print("Missing repo:", repo_dir)
            return 1
        for subdir in REQUIRED_SUBDIRS:
            if not (repo_dir / subdir).exists():
                print(f"Missing {subdir} in {repo}")
                return 1
        if not (repo_dir / "README.md").exists():
            print(f"Missing README in {repo}")
            return 1
        if not (repo_dir / "docs" / "OVERVIEW.md").exists():
            print(f"Missing OVERVIEW in {repo}")
            return 1
        if not (repo_dir / "ops" / "RUNBOOK.md").exists():
            print(f"Missing RUNBOOK in {repo}")
            return 1

    print("HeadyMusic + HeadySymphony scaffold validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
