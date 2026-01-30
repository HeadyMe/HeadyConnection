# HeadyPoPS Oracle

Local-only telemetry ingestion schema for Proof-of-Possession (PoPS) oracle events.

## Assets
- `schema.json` defines the ingestion payload contract.
- `sample_payload.json` provides a deterministic example payload.

## Validation
```bash
python3 scripts/crypto/validate_pops_oracle.py crypto/pops_oracle/sample_payload.json
```

## Next Steps
- Implement signature verification using managed keys.
- Integrate policy gating in the governance pipeline.
