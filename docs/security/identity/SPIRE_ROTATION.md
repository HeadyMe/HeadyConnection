# SPIRE CA Rotation SOP

1. Schedule rotation window with stakeholders.
2. Generate new CA bundle.
3. Update SPIRE server config and restart.
4. Verify workloads obtain new SVIDs.

## Verification
- `spire-server bundle show`
- `spire-agent healthcheck`
