# Post-Generation Notes

- Governance policies are consumed from the canonical governance repo via `governance.lock.json`.
- Run `scripts/governance/install_policy_pack.sh` after updating the lock file with the real release asset.
- Configure Cloudflare Tunnel credentials outside the repo.
- Update SPIFFE/SPIRE trust domain values once the canonical domain is finalized.
