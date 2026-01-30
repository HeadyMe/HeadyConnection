# HeadyKinetic (Kinetic Governance)

Prototype module that simulates thermal verification of actuator and RF activity to detect kinetic drift or unauthorized transmission.

## Demo
```bash
python3 apps/heady_kinetic/kinetic_governance.py --demo
```

## Custom Input
```bash
python3 apps/heady_kinetic/kinetic_governance.py --input kinetic_payload.json --output kinetic_report.json --timestamp 2026-04-06T00:00:00Z
```

Example payload:
```json
{
  "agent_state": "STATIONARY",
  "comms_state": "RADIO_SILENCE",
  "policy": {
    "stationary_state": "STATIONARY",
    "radio_silence_state": "RADIO_SILENCE"
  },
  "actuators": [
    { "name": "rotor_3", "thermal_c": 68.0, "resting_floor_c": 40.0, "threshold_delta_c": 6.0 }
  ],
  "rf_modules": [
    { "name": "rf_amp_a", "thermal_c": 55.0, "resting_floor_c": 35.0, "threshold_delta_c": 4.0 }
  ]
}
```

## Notes
- Emits a proof-of-state hash for audit trails.
- Replace thresholds with calibrated field data and ruggedized sensors.
