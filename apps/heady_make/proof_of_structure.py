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
class LayerScan:
    layer_index: int
    scan_payload: str
    cad_payload: str


@dataclass
class LayerAttestation:
    layer_index: int
    scan_hash: str
    cad_hash: str
    match: bool
    signed_at: str
    signature: str


def hash_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sign_attestation(scan_hash: str, cad_hash: str) -> str:
    material = f"{scan_hash}:{cad_hash}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def attest_layers(scans: Iterable[LayerScan]) -> list[LayerAttestation]:
    attestations: list[LayerAttestation] = []
    for scan in scans:
        scan_hash = hash_payload(scan.scan_payload)
        cad_hash = hash_payload(scan.cad_payload)
        match = scan_hash == cad_hash
        signature = sign_attestation(scan_hash, cad_hash)
        attestations.append(
            LayerAttestation(
                layer_index=scan.layer_index,
                scan_hash=scan_hash,
                cad_hash=cad_hash,
                match=match,
                signed_at=datetime.utcnow().isoformat() + "Z",
                signature=signature,
            )
        )
    return attestations


def load_scans(path: Path) -> list[LayerScan]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw_scans = raw.get("scans", [])
    elif isinstance(raw, list):
        raw_scans = raw
    else:
        raise ValueError("Input JSON must be a list or an object with a 'scans' list.")

    scans: list[LayerScan] = []
    for entry in raw_scans:
        scans.append(
            LayerScan(
                layer_index=int(entry["layer_index"]),
                scan_payload=str(entry["scan_payload"]),
                cad_payload=str(entry["cad_payload"]),
            )
        )
    return scans


def emit_attestations(attestations: list[LayerAttestation], output: Path | None) -> None:
    payload = json.dumps([att.__dict__ for att in attestations], indent=2)
    if output:
        output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def demo() -> int:
    scans = [
        LayerScan(layer_index=1, scan_payload="layer-1-scan", cad_payload="layer-1-scan"),
        LayerScan(layer_index=2, scan_payload="layer-2-scan", cad_payload="layer-2-cad"),
    ]
    attestations = attest_layers(scans)
    emit_attestations(attestations, None)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HeadyMake Proof-of-Structure demo")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--input", type=Path, help="Path to JSON scan inputs")
    parser.add_argument("--output", type=Path, help="Write attestations to a JSON file")
    args = parser.parse_args()

    if args.input:
        scans = load_scans(args.input)
        attestations = attest_layers(scans)
        emit_attestations(attestations, args.output)
        return 0

    if args.demo:
        return demo()

    print("Run with --demo to generate sample attestations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
