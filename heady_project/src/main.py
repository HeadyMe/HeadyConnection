from __future__ import annotations

import argparse
import json
from pathlib import Path

from throttle import ComputeThrottle
from verticals.bio import EphemeralProcessor
from verticals.mint import TokenIssuer
from verticals.symphony import NarrativeToMIDI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Heady Federation vertical runner.")
    parser.add_argument("--run-symphony", action="store_true", help="Run the HeadySymphony vertical demo.")
    parser.add_argument("--run-bio", action="store_true", help="Run the HeadyBio vertical demo.")
    parser.add_argument("--run-mint", action="store_true", help="Run the HeadyMint vertical demo.")
    parser.add_argument("--narrative", default="Melancholy Rain", help="Narrative prompt for Symphony.")
    parser.add_argument("--payload", default="pulse-data", help="Payload for Bio (string).")
    parser.add_argument("--work-signal", type=float, default=42.0, help="Work signal for Mint.")
    parser.add_argument(
        "--ledger-path",
        default=str(Path("heady_project/data/mint/ledger.jsonl")),
        help="Ledger path for Mint.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    throttle = ComputeThrottle()
    outputs = {}

    if args.run_symphony:
        symphony = NarrativeToMIDI(throttle=throttle)
        outputs["symphony"] = symphony.render(args.narrative)
    if args.run_bio:
        bio = EphemeralProcessor(throttle=throttle)
        outputs["bio"] = bio.process(args.payload.encode("utf-8"))
    if args.run_mint:
        mint = TokenIssuer(throttle=throttle, ledger_path=Path(args.ledger_path))
        outputs["mint"] = mint.issue(args.work_signal)

    if not outputs:
        print("No vertical selected. Use --run-symphony, --run-bio, or --run-mint.")
        return 1
    print(json.dumps(outputs, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
