# HeadyField (Regenerative Oracle)

Prototype module that simulates soil telemetry scoring and payout gating.

## Demo
```bash
python3 apps/heady_field/regenerative_oracle.py --demo
```

## Custom Input
```bash
python3 apps/heady_field/regenerative_oracle.py --input telemetry.json --output oracle_report.json
```

Example payload:
```json
{
  "nitrogen_ppm": 18.5,
  "moisture_pct": 42.0,
  "mycelium_index": 88.0,
  "timestamp": "2026-04-06T00:00:00Z"
}
```

## Notes
- Uses signed sample payloads for verification.
- Replace the scoring thresholds with calibrated agronomy values.
