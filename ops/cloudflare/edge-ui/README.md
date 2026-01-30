# Edge UI Worker Template

This template serves a lightweight status page from the edge. It is intended for public status UI while privileged operations remain on the tunnel-only origin.

## Usage
1. Copy `wrangler.toml.example` to `wrangler.toml` and set `STATUS_FEED_URL`.
2. Deploy via Wrangler.
3. Point a public hostname to the worker route.

## Status Feed
The worker expects a JSON payload with `status`, `summary`, and optional `updated_at` fields. Example:

```json
{
  "status": "ok",
  "summary": "All systems operational",
  "updated_at": "2026-04-01T00:00:00Z"
}
```

## Governance Notes
- Keep `STATUS_FEED_URL` on an allowlisted origin.
- Avoid sensitive data in public status responses.
- Coordinate cache TTL with incident response workflows.
