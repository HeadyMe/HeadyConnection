# Edge UI Termination

Edge UI termination serves public or low-risk UI fragments directly at the edge to reduce round-trip latency to the origin. This enables faster page loads while keeping sensitive operations on the tunnel-only origin.

## Targets
- Public marketing pages or documentation.
- Low-risk, cacheable UI fragments.
- Status pages and uptime banners.

## Required Safeguards
- Signed requests from edge to origin for any privileged data.
- Origin allowlist enforcement (host + origin headers).
- Cache invalidation tied to governance updates.

## Suggested Architecture
1. Cloudflare Worker renders or streams edge UI.
2. Worker fetches status JSON from a local feed (if needed).
3. Privileged operations proxy to the origin with a signed request.

## Operational Checklist
- Keep edge worker source-controlled and reviewed.
- Limit secrets in edge environments.
- Monitor cache hit ratio and error budgets.
