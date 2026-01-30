#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class ActuatorReading:
    name: str
    thermal_c: float
    resting_floor_c: float
    threshold_delta_c: float


@dataclass
class RfReading:
    name: str
    thermal_c: float
    resting_floor_c: float
    threshold_delta_c: float


@dataclass
class KineticPolicy:
    stationary_state: str
    radio_silence_state: str


def hash_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def resolve_timestamp(value: str | None) -> str:
    if value:
        return value
    return datetime.utcnow().isoformat() + "Z"


def parse_actuators(items: Iterable[dict]) -> list[ActuatorReading]:
    readings: list[ActuatorReading] = []
    for item in items:
        readings.append(
            ActuatorReading(
                name=str(item["name"]),
                thermal_c=float(item["thermal_c"]),
                resting_floor_c=float(item["resting_floor_c"]),
                threshold_delta_c=float(item.get("threshold_delta_c", 4.0)),
            )
        )
    return readings


def parse_rf(items: Iterable[dict]) -> list[RfReading]:
    readings: list[RfReading] = []
    for item in items:
        readings.append(
            RfReading(
                name=str(item["name"]),
                thermal_c=float(item["thermal_c"]),
                resting_floor_c=float(item["resting_floor_c"]),
                threshold_delta_c=float(item.get("threshold_delta_c", 3.0)),
            )
        )
    return readings


def evaluate_kinetic_drift(
    agent_state: str, policy: KineticPolicy, actuators: Iterable[ActuatorReading]
) -> list[dict]:
    alerts: list[dict] = []
    if agent_state != policy.stationary_state:
        return alerts
    for actuator in actuators:
        if actuator.thermal_c > actuator.resting_floor_c + actuator.threshold_delta_c:
            alerts.append(
                {
                    "type": "KINETIC_DRIFT_DETECTED",
                    "target": actuator.name,
                    "observed_c": actuator.thermal_c,
                    "floor_c": actuator.resting_floor_c,
                    "threshold_delta_c": actuator.threshold_delta_c,
                    "recommended_action": "HARD_CUTOFF",
                }
            )
    return alerts


def evaluate_radio_silence(
    comms_state: str, policy: KineticPolicy, rf_modules: Iterable[RfReading]
) -> list[dict]:
    alerts: list[dict] = []
    if comms_state != policy.radio_silence_state:
        return alerts
    for rf in rf_modules:
        if rf.thermal_c > rf.resting_floor_c + rf.threshold_delta_c:
            alerts.append(
                {
                    "type": "UNAUTHORIZED_TRANSMISSION",
                    "target": rf.name,
                    "observed_c": rf.thermal_c,
                    "floor_c": rf.resting_floor_c,
                    "threshold_delta_c": rf.threshold_delta_c,
                    "recommended_action": "ANTENNA_SEVER",
                }
            )
    return alerts


def build_report(payload: dict, generated_at: str | None = None) -> dict:
    policy = KineticPolicy(
        stationary_state=str(payload.get("policy", {}).get("stationary_state", "STATIONARY")),
        radio_silence_state=str(payload.get("policy", {}).get("radio_silence_state", "RADIO_SILENCE")),
    )
    agent_state = str(payload.get("agent_state", "UNKNOWN"))
    comms_state = str(payload.get("comms_state", "UNKNOWN"))
    actuators = parse_actuators(payload.get("actuators", []))
    rf_modules = parse_rf(payload.get("rf_modules", []))

    kinetic_alerts = evaluate_kinetic_drift(agent_state, policy, actuators)
    rf_alerts = evaluate_radio_silence(comms_state, policy, rf_modules)
    alerts = kinetic_alerts + rf_alerts

    report = {
        "agent_state": agent_state,
        "comms_state": comms_state,
        "policy": policy.__dict__,
        "alerts": alerts,
        "alert_count": len(alerts),
        "generated_at": resolve_timestamp(generated_at),
    }
    report["proof_of_state"] = hash_payload(json.dumps(report, sort_keys=True))
    return report


def emit_report(report: dict, output: Path | None) -> None:
    payload = json.dumps(report, indent=2)
    if output:
        output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def demo() -> int:
    payload = {
        "agent_state": "STATIONARY",
        "comms_state": "RADIO_SILENCE",
        "policy": {"stationary_state": "STATIONARY", "radio_silence_state": "RADIO_SILENCE"},
        "actuators": [
            {"name": "rotor_3", "thermal_c": 68.0, "resting_floor_c": 40.0, "threshold_delta_c": 6.0}
        ],
        "rf_modules": [
            {"name": "rf_amp_a", "thermal_c": 55.0, "resting_floor_c": 35.0, "threshold_delta_c": 4.0}
        ],
    }
    report = build_report(payload)
    emit_report(report, None)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HeadyKinetic kinetic governance demo")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--input", type=Path, help="Path to kinetic telemetry JSON")
    parser.add_argument("--output", type=Path, help="Write report to JSON")
    parser.add_argument("--timestamp", type=str, help="Override generated_at timestamp for deterministic runs")
    args = parser.parse_args()

    if args.input:
        payload = load_payload(args.input)
        report = build_report(payload, generated_at=args.timestamp)
        emit_report(report, args.output)
        return 0

    if args.demo:
        return demo()

    print("Run with --demo or provide --input to generate a report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
