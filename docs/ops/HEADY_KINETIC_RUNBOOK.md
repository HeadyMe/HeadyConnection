# HeadyKinetic Runbook

Operational guidance for deploying and validating the HeadyKinetic kinetic governance module.

## Scope
HeadyKinetic validates actuator and RF thermal emissions on edge devices. It does **not** transmit raw thermal telemetry outside the device boundary unless explicitly configured.

## Safety Guidelines
- Calibrate thermal floors per device and environment.
- Use redundant sensors for critical actuators.
- Treat alerts as safety-critical and integrate with hardware cutoffs.

## Validation
```bash
python3 apps/heady_kinetic/kinetic_governance.py --demo
python3 scripts/ops/validate_heady_kinetic.py
```

## Rollback
Disable the HeadyKinetic module and revert to software-only telemetry checks if sensor hardware is unavailable.
