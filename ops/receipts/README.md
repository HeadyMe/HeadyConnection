# Change Receipts

This folder stores cryptographic receipts for significant logic or parameter changes.

## Process
1. Build a receipt payload (JSON) describing the change, rationale, risks, and rollback.
2. Sign the payload using an ephemeral Ed25519 key.
3. Store the receipt payload and signature in `receipts.jsonl` alongside the public key.

## Validation
```bash
python3 scripts/ops/validate_receipts.py ops/receipts/receipts.jsonl
```

> Note: For production, replace ephemeral signing with managed keys/HSM.
