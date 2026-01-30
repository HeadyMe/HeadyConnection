# Rollback Playbook

1. Identify the failing change.
2. Roll back the deployment to the last known good version.
3. Verify health endpoints and docs validation.
4. Document incident and root cause.

## Verification
- `python3 scripts/docs/validate_docs.py`
- Service `/health` endpoints return `ok`.
