#!/usr/bin/env python3
"""Scaffold generator for HeadyMusic + HeadySymphony repos.

This script emits a deterministic starter layout for a standalone music vertical. It does not
fetch external dependencies and only writes metadata-first scaffolding that can be expanded
into full repos later.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "heady_music_symphony"


@dataclass(frozen=True)
class RepoSpec:
    name: str
    description: str
    folders: tuple[str, ...]


REPOS = (
    RepoSpec(
        name="heady-music",
        description="Music runtime services, audio processing, and UX scaffolding.",
        folders=("app", "docs", "ops", "scripts"),
    ),
    RepoSpec(
        name="heady-symphony",
        description="HeadySymphony core generation pipeline and API scaffolding.",
        folders=("app", "docs", "ops", "scripts"),
    ),
)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []

    for repo in REPOS:
        repo_dir = OUTPUT_DIR / repo.name
        repo_dir.mkdir(parents=True, exist_ok=True)

        for folder in repo.folders:
            (repo_dir / folder).mkdir(parents=True, exist_ok=True)

        write_text(
            repo_dir / "README.md",
            f"# {repo.name}\n\n{repo.description}\n\n"
            "## Next Steps\n"
            "- Add runtime services and API contracts.\n"
            "- Define storage and processing boundaries.\n"
            "- Document compliance and data isolation.\n",
        )

        write_text(
            repo_dir / "docs" / "OVERVIEW.md",
            "# Overview\n\nThis is a scaffolded repository for HeadyMusic/HeadySymphony."
            "\n\n## Data Isolation\nKeep audio processing isolated per vertical and exchange only non-sensitive metadata.\n",
        )

        write_text(
            repo_dir / "ops" / "RUNBOOK.md",
            "# Operations Runbook\n\nLocal-first scaffolding only. Extend with service orchestration when ready.\n",
        )

        manifest.append({"name": repo.name, "description": repo.description})

    write_text(
        OUTPUT_DIR / "manifest.json",
        json.dumps({"generated_by": "HeadyMusic_HeadySymphony_v_1_0_0.py", "repos": manifest}, indent=2),
    )

    print(f"Scaffold written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
