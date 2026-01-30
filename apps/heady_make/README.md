# HeadyMake (Proof-of-Structure)

Prototype module that simulates layer-by-layer scan hashing for additive manufacturing.

## Demo
```bash
python3 apps/heady_make/proof_of_structure.py --demo
```

## Custom Input
```bash
python3 apps/heady_make/proof_of_structure.py --input scans.json --output attestations.json
```

Input JSON can be a list of scans or an object with a `scans` list:
```json
{
  "scans": [
    { "layer_index": 1, "scan_payload": "layer-1-scan", "cad_payload": "layer-1-scan" }
  ]
}
```

## Notes
- Emits signed layer attestations in-memory for demonstration.
- Replace the signing stub with hardware-backed keys in production.
