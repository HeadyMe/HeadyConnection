#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD|PLACEHOLDER|REPLACE_ME|REPLACE|EXAMPLE|YOURORG)\b", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge iteration context dumps into a single release context file.")
    parser.add_argument(
        "--inputs",
        nargs="+",
        help="Context dump JSON files to merge. Defaults to heady_iterations/it*/manifest.json",
    )
    parser.add_argument(
        "--iterations-dir",
        default="heady_iterations",
        help="Directory holding iteration outputs (default: heady_iterations)",
    )
    parser.add_argument(
        "--output",
        default="heady_iterations/context_dump_merged.json",
        help="Output path for merged context dump",
    )
    parser.add_argument(
        "--placeholder",
        action="append",
        default=[],
        help="Placeholder replacement in TOKEN=VALUE form. Can be provided multiple times.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow unresolved placeholders to remain in the merged output",
    )
    parser.add_argument(
        "--ip-artifact",
        action="append",
        default=[],
        help="Path to an IP capture artifact to hash (repeatable).",
    )
    parser.add_argument(
        "--ip-note",
        action="append",
        default=[],
        help="Free-form note to include in the IP capture block (repeatable).",
    )
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing context dump: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Context dump must be a JSON object: {path}")
    return data


def find_default_inputs(iterations_dir: Path) -> list[Path]:
    manifest_paths = sorted(iterations_dir.glob("it*/manifest.json"))
    if not manifest_paths:
        raise SystemExit(f"No iteration manifests found in {iterations_dir}")
    return manifest_paths


def parse_replacements(items: Iterable[str]) -> dict[str, str]:
    replacements: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Placeholder replacement must be TOKEN=VALUE: {item}")
        token, value = item.split("=", 1)
        token = token.strip()
        if not token:
            raise SystemExit(f"Placeholder token cannot be empty: {item}")
        replacements[token] = value
    return replacements


def resolve_placeholders(value: Any, replacements: dict[str, str], path: str, unresolved: list[dict[str, str]]) -> Any:
    if isinstance(value, dict):
        return {k: resolve_placeholders(v, replacements, f"{path}.{k}", unresolved) for k, v in value.items()}
    if isinstance(value, list):
        return [
            resolve_placeholders(item, replacements, f"{path}[{index}]", unresolved)
            for index, item in enumerate(value)
        ]
    if isinstance(value, str):
        updated = value
        for token, replacement in replacements.items():
            token_re = re.compile(re.escape(token), re.IGNORECASE)
            updated = token_re.sub(replacement, updated)
        if PLACEHOLDER_PATTERN.search(updated):
            unresolved.append({"path": path, "value": value})
        return updated
    return value


def hash_artifact(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing IP artifact: {path}")
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    stat = path.stat()
    return {
        "path": path.as_posix(),
        "sha256": digest,
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
    }


def build_output(entries: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    entries_sorted = sorted(entries, key=lambda item: (item[1].get("iteration", 0), item[0].as_posix()))
    sources = []
    iterations = []
    for path, data in entries_sorted:
        sources.append(
            {
                "path": path.as_posix(),
                "iteration": data.get("iteration"),
                "stage_name": data.get("stage_name"),
                "version": data.get("version"),
                "summary": data.get("summary"),
            }
        )
        iterations.append(data)
    return {
        "schema_version": "1.0.0",
        "generated_at": utc_now(),
        "source_count": len(entries_sorted),
        "sources": sources,
        "iterations": iterations,
    }


def main() -> int:
    args = parse_args()
    iterations_dir = Path(args.iterations_dir)
    output_path = Path(args.output)
    input_paths = [Path(item) for item in args.inputs] if args.inputs else find_default_inputs(iterations_dir)
    entries = [(path, load_json(path)) for path in input_paths]

    merged = build_output(entries)
    if args.ip_artifact or args.ip_note:
        merged["ip_capture"] = {
            "generated_at": utc_now(),
            "artifacts": [hash_artifact(Path(item)) for item in args.ip_artifact],
            "notes": list(args.ip_note),
        }

    replacements = parse_replacements(args.placeholder)
    unresolved: list[dict[str, str]] = []
    resolved = resolve_placeholders(merged, replacements, "root", unresolved)
    resolved["placeholder_resolution"] = {
        "replacements": replacements,
        "unresolved_count": len(unresolved),
        "unresolved": unresolved,
    }

    if unresolved and not args.allow_placeholders:
        print("Unresolved placeholders detected:")
        for item in unresolved:
            print(f"- {item['path']}: {item['value']}")
        print("Provide --placeholder replacements or --allow-placeholders to proceed.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(resolved, indent=2) + "\n", encoding="utf-8")
    print(f"Merged context dump written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
