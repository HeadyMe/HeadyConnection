# SPIRE Ops

This directory contains SPIRE server and agent configuration scaffolding.

## Files
- `server/server.conf`
- `agent/agent.conf`
- `register_workloads.sh`

## Notes
Update the trust domain before production rollout.

## Usage
```bash
./register_workloads.sh
```

### Environment Overrides
```bash
SPIFFE_ID=spiffe://your.domain/ns/prod/sa/api \
SELECTORS="k8s:ns:prod,k8s:sa:api" \
./register_workloads.sh
```
