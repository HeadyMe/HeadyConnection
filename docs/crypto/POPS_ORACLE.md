# PoPS Oracle (Telemetry Ingestion)

This document defines the Proof-of-Possession (PoPS) oracle payload contract and validation workflow for telemetry ingestion.

## Schema
The canonical schema lives at `crypto/pops_oracle/schema.json`.

## Sample Payload
Use the deterministic example payload for validation:
```bash
python3 scripts/crypto/validate_pops_oracle.py crypto/pops_oracle/sample_payload.json
```

## Governance Notes
- Payloads are metadata-only; no cross-vertical sharing.
- Signature verification is required before production ingestion.
