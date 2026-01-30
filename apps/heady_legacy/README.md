# HeadyLegacy (Sovereign Succession)

Prototype module that simulates biometric inactivity checks and shard recovery requirements.

## Demo
```bash
python3 apps/heady_legacy/sovereign_succession.py --demo
```

## Custom Input
```bash
python3 apps/heady_legacy/sovereign_succession.py --input succession.json --as-of 2026-04-06T00:00:00Z --output status.json
```

Example payload:
```json
{
  "policy": {
    "inactivity_days": 30,
    "shard_threshold": 3,
    "total_shards": 5
  },
  "last_check_in": "2026-03-01T00:00:00Z",
  "shards_collected": 3
}
```

## Notes
- Demonstrates Shamir-style quorum checks without real key material.
- Integrate with biometric sensors and MPC services for production use.
