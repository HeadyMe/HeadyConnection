#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class SuccessionPolicy:
    inactivity_days: int
    shard_threshold: int
    total_shards: int


@dataclass
class SuccessionStatus:
    last_check_in: str
    inactivity_days: int
    eligible: bool
    shards_collected: int
    shard_threshold: int


def evaluate_policy(
    policy: SuccessionPolicy,
    last_check_in: datetime,
    shards_collected: int,
    now: datetime | None = None,
) -> SuccessionStatus:
    effective_now = now or datetime.utcnow()
    inactivity_days = (effective_now - last_check_in).days
    eligible = inactivity_days >= policy.inactivity_days and shards_collected >= policy.shard_threshold
    return SuccessionStatus(
        last_check_in=last_check_in.isoformat() + "Z",
        inactivity_days=inactivity_days,
        eligible=eligible,
        shards_collected=shards_collected,
        shard_threshold=policy.shard_threshold,
    )


def parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def load_request(path: Path, as_of: datetime | None) -> tuple[SuccessionPolicy, datetime, int, datetime]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    policy = SuccessionPolicy(
        inactivity_days=int(raw["policy"]["inactivity_days"]),
        shard_threshold=int(raw["policy"]["shard_threshold"]),
        total_shards=int(raw["policy"]["total_shards"]),
    )
    last_check_in = parse_timestamp(str(raw["last_check_in"]))
    shards_collected = int(raw["shards_collected"])
    effective_now = as_of or datetime.utcnow()
    return policy, last_check_in, shards_collected, effective_now


def emit_status(status: SuccessionStatus, output: Path | None) -> None:
    payload = json.dumps(status.__dict__, indent=2)
    if output:
        output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def demo() -> int:
    policy = SuccessionPolicy(inactivity_days=30, shard_threshold=3, total_shards=5)
    last_check_in = datetime.utcnow() - timedelta(days=32)
    status = evaluate_policy(policy, last_check_in, shards_collected=3)
    emit_status(status, None)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HeadyLegacy Sovereign Succession demo")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--input", type=Path, help="Path to JSON succession request")
    parser.add_argument("--as-of", type=str, help="ISO timestamp to evaluate against")
    parser.add_argument("--output", type=Path, help="Write succession status to a JSON file")
    args = parser.parse_args()

    if args.input:
        as_of = parse_timestamp(args.as_of) if args.as_of else None
        policy, last_check_in, shards_collected, effective_now = load_request(args.input, as_of)
        status = evaluate_policy(policy, last_check_in, shards_collected, now=effective_now)
        emit_status(status, args.output)
        return 0

    if args.demo:
        return demo()

    print("Run with --demo to generate a sample succession status.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
