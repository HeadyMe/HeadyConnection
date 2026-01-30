#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPTS = ROOT / "ops" / "receipts" / "receipts.jsonl"
PUBLIC_KEY = ROOT / "ops" / "receipts" / "public_key.pem"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a signed receipt for a change.")
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--files", required=True, help="Comma-separated list of files")
    parser.add_argument("--risk", required=True)
    parser.add_argument("--rollback", required=True)
    args = parser.parse_args()

    payload = {
        "change_id": args.change_id,
        "summary": args.summary,
        "files": [f.strip() for f in args.files.split(",") if f.strip()],
        "risk": args.risk,
        "rollback": args.rollback,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        key_path = tmpdir_path / "receipt_key.pem"
        payload_path = tmpdir_path / "payload.json"
        sig_path = tmpdir_path / "payload.sig"

        payload_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")

        run(["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(key_path)])
        run(["openssl", "pkey", "-in", str(key_path), "-pubout", "-out", str(PUBLIC_KEY)])
        run([
            "openssl",
            "pkeyutl",
            "-sign",
            "-rawin",
            "-inkey",
            str(key_path),
            "-in",
            str(payload_path),
            "-out",
            str(sig_path),
        ])

        signature = base64.b64encode(sig_path.read_bytes()).decode("ascii")

    receipt_entry = {
        "payload": payload,
        "signature": signature,
        "public_key": PUBLIC_KEY.read_text(encoding="utf-8"),
    }

    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    with RECEIPTS.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt_entry) + "\n")

    print(f"Recorded receipt {args.change_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
