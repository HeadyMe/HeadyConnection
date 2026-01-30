#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Iterable


class GitError(RuntimeError):
    pass


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def ensure_repo(repo: Path) -> None:
    run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo)


def ensure_branches(repo: Path, branches: Iterable[str]) -> None:
    for branch in branches:
        run(["git", "rev-parse", "--verify", branch], cwd=repo)


def ahead_counts(repo: Path, base: str, other: str) -> tuple[int, int]:
    output = run(["git", "rev-list", "--left-right", "--count", f"{base}...{other}"], cwd=repo)
    left, right = output.split()
    return int(left), int(right)


def changed_files(repo: Path, base: str, other: str) -> list[str]:
    output = run(["git", "diff", "--name-only", f"{base}..{other}"], cwd=repo)
    return [line for line in output.splitlines() if line.strip()]


def select_base_branch(repo: Path, branches: list[str]) -> str:
    scores = {}
    for candidate in branches:
        total_ahead = 0
        for other in branches:
            if other == candidate:
                continue
            _, ahead = ahead_counts(repo, candidate, other)
            total_ahead += ahead
        scores[candidate] = total_ahead
    return min(scores, key=scores.get)


def build_plan(repo: Path, branches: list[str]) -> dict:
    base_branch = select_base_branch(repo, branches)
    branch_details: dict[str, dict] = {}
    overlap_map: dict[str, set[str]] = {}

    for branch in branches:
        if branch == base_branch:
            branch_details[branch] = {"ahead_commits": 0, "files_changed": [], "overlap_count": 0}
            continue
        _, ahead = ahead_counts(repo, base_branch, branch)
        files = changed_files(repo, base_branch, branch)
        branch_details[branch] = {"ahead_commits": ahead, "files_changed": files, "overlap_count": 0}
        for filename in files:
            overlap_map.setdefault(filename, set()).add(branch)

    for filename, owners in overlap_map.items():
        if len(owners) > 1:
            for branch in owners:
                branch_details[branch]["overlap_count"] += 1

    merge_order = [
        branch
        for branch in sorted(
            [b for b in branches if b != base_branch],
            key=lambda b: (branch_details[b]["overlap_count"], branch_details[b]["ahead_commits"], b),
        )
    ]

    overlap_files = [
        {"file": filename, "branches": sorted(list(owners)), "count": len(owners)}
        for filename, owners in sorted(overlap_map.items())
        if len(owners) > 1
    ]

    return {
        "repo": str(repo),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "base_branch": base_branch,
        "merge_order": merge_order,
        "branches": branch_details,
        "overlap_files": overlap_files,
        "notes": [
            "Review overlap_files for conflict hotspots.",
            "Use --execute to merge in a temporary worktree.",
        ],
    }


def write_plan(plan: dict, output: Path | None) -> None:
    payload = json.dumps(plan, indent=2)
    if output:
        output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def execute_plan(repo: Path, plan: dict, strategy: str) -> str:
    base_branch = plan["base_branch"]
    merge_order = plan["merge_order"]
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    target_branch = f"combined/{timestamp}"

    with tempfile.TemporaryDirectory() as tmpdir:
        worktree = Path(tmpdir) / "merge-worktree"
        run(["git", "worktree", "add", str(worktree), base_branch], cwd=repo)
        try:
            run(["git", "checkout", "-b", target_branch], cwd=worktree)
            for branch in merge_order:
                run(["git", "merge", "--no-ff", f"--strategy={strategy}", branch], cwd=worktree)
        finally:
            run(["git", "worktree", "remove", "--force", str(worktree)], cwd=repo)

    return target_branch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan and execute branch consolidation in a safe worktree.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Path to the repo root")
    parser.add_argument("--branches", nargs="+", required=True, help="Branches to consolidate")
    parser.add_argument("--output", type=Path, help="Write plan JSON to this file")
    parser.add_argument("--execute", action="store_true", help="Execute the consolidation plan")
    parser.add_argument("--strategy", default="recursive", help="Git merge strategy (default: recursive)")
    parser.add_argument("--allow-single", action="store_true", help="Allow a single branch for dry-run validation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    ensure_repo(repo)

    if len(args.branches) < 2 and not args.allow_single:
        raise SystemExit("Provide at least two branches (or pass --allow-single for dry-run validation).")

    ensure_branches(repo, args.branches)
    plan = build_plan(repo, args.branches)
    write_plan(plan, args.output)

    if args.execute:
        target_branch = execute_plan(repo, plan, args.strategy)
        print(f"Consolidation branch created: {target_branch}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
