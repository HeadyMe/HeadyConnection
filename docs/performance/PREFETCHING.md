# Predictive Prefetching

Predictive prefetching (Tempo Engine) pre-loads likely assets or metadata before a user explicitly requests them. The goal is to reduce perceived latency without violating data-minimization policies.

## Principles
- **Privacy-first:** Only prefetch assets derived from allowlisted signals.
- **Soft prefetch:** Cache metadata or public assets first; never fetch sensitive content without explicit request.
- **Expiry-aware:** Use short TTLs and purge on policy changes.

## Example Workflow
1. Intel Edge worker scores likely next assets.
2. Tempo Engine issues a prefetch hint.
3. Edge cache warms public assets with signed receipts.
4. Origin retains final authority for privileged content.

## Policy Hooks
- Require allowlist approval for any signal that drives prefetch.
- Track prefetch decisions in audit logs.
- Disable prefetch for sensitive verticals by default.
