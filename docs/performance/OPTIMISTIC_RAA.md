# Optimistic RAA Execution

Optimistic RAA execution allows low-risk actions to start immediately while policy verification runs in parallel. If verification fails, the system performs a deterministic rollback and records the failure for auditing.

## When to Use
- Actions classified as low-risk with bounded side effects.
- Operations that can be rolled back deterministically.
- Workflows where latency is more costly than immediate consistency.

## Guardrails
1. **Risk threshold:** Restrict optimistic execution to actions explicitly tagged as low-risk.
2. **Rollback capability:** Require deterministic undo or snapshot restore.
3. **Receipts:** Always emit an optimistic receipt and a verification receipt.
4. **Audit trail:** Log the request, optimistic grant, verification outcome, and rollback steps.

## Suggested Data Contract
```json
{
  "status": "optimistic",
  "risk_score": 1,
  "receipt_id": "raa_2026_04_01_0001",
  "verification_deadline": "2026-04-01T00:00:10Z"
}
```

## Operational Notes
- Ensure on-call runbooks specify rollback automation paths.
- Train monitoring to alert on verification failures or rollback loops.
- Keep a hard fail-safe in case verification cannot complete.
