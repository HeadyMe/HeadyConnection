#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class SoilTelemetry:
    nitrogen_ppm: float
    moisture_pct: float
    mycelium_index: float
    timestamp: str


def score_telemetry(data: SoilTelemetry) -> float:
    return round((data.nitrogen_ppm * 0.4) + (data.moisture_pct * 0.3) + (data.mycelium_index * 0.3), 2)


def sign_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_telemetry(path: Path) -> SoilTelemetry:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return SoilTelemetry(
        nitrogen_ppm=float(raw["nitrogen_ppm"]),
        moisture_pct=float(raw["moisture_pct"]),
        mycelium_index=float(raw["mycelium_index"]),
        timestamp=str(raw.get("timestamp") or datetime.utcnow().isoformat() + "Z"),
    )


def emit_report(telemetry: SoilTelemetry, output: Path | None) -> None:
    score = score_telemetry(telemetry)
    payload = json.dumps(telemetry.__dict__, sort_keys=True)
    signature = sign_payload(payload)
    payout_ready = score >= 50
    report = {
        "telemetry": telemetry.__dict__,
        "score": score,
        "payout_ready": payout_ready,
        "signature": signature,
    }
    payload_json = json.dumps(report, indent=2)
    if output:
        output.write_text(payload_json + "\n", encoding="utf-8")
    else:
        print(payload_json)


def demo() -> int:
    telemetry = SoilTelemetry(nitrogen_ppm=18.5, moisture_pct=42.0, mycelium_index=88.0, timestamp=datetime.utcnow().isoformat() + "Z")
    emit_report(telemetry, None)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HeadyField Regenerative Oracle demo")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--input", type=Path, help="Path to JSON telemetry input")
    parser.add_argument("--output", type=Path, help="Write oracle report to a JSON file")
    args = parser.parse_args()

    if args.input:
        telemetry = load_telemetry(args.input)
        emit_report(telemetry, args.output)
        return 0

    if args.demo:
        return demo()

    print("Run with --demo to generate sample telemetry scores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
