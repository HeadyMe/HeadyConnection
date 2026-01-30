from __future__ import annotations

import argparse
import json
from pathlib import Path

from throttle import ComputeThrottle
from verticals.bio import EphemeralProcessor
from verticals.mint import TokenIssuer
from verticals.symphony import NarrativeToMIDI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Heady admin console.")
    parser.add_argument("--run-symphony", action="store_true", help="Trigger Symphony vertical.")
    parser.add_argument("--run-bio", action="store_true", help="Trigger Bio vertical.")
    parser.add_argument("--run-mint", action="store_true", help="Trigger Mint vertical.")
    parser.add_argument("--narrative", default="Distant Horizon", help="Narrative prompt for Symphony.")
    parser.add_argument("--payload", default="ephemeral-scan", help="Payload for Bio (string).")
    parser.add_argument("--work-signal", type=float, default=10.0, help="Work signal for Mint.")
    parser.add_argument(
        "--ledger-path",
        default=str(Path("heady_project/data/mint/ledger.jsonl")),
        help="Ledger path for Mint.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    throttle = ComputeThrottle()
    actions = {}

    if args.run_symphony:
        actions["symphony"] = NarrativeToMIDI(throttle).render(args.narrative)
    if args.run_bio:
        actions["bio"] = EphemeralProcessor(throttle).process(args.payload.encode("utf-8"))
    if args.run_mint:
        actions["mint"] = TokenIssuer(throttle, Path(args.ledger_path)).issue(args.work_signal)

    if not actions:
        print("No action selected. Use --run-symphony, --run-bio, or --run-mint.")
        return 1
    print(json.dumps(actions, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
