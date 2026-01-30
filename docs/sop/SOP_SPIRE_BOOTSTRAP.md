# SOP: SPIRE Bootstrap

1. Provision SPIRE server host and storage.
2. Update trust domain values in `ops/spire/server/server.conf` and `ops/spire/agent/agent.conf`.
3. Start SPIRE server and agent.
4. Run `ops/spire/register_workloads.sh` with real selectors.
5. Validate entries using `spire-server entry show`.

> NOTE: Replace placeholder trust domains before production use.
