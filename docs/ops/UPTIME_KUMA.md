# Uptime Kuma Integration

Uptime Kuma provides self-hosted uptime monitoring and status pages. This stack is intended for internal monitoring with a local status feed that can be consumed by the Trust Center module.

## Compose Scaffold
Use the ops compose scaffold to launch Uptime Kuma locally:

```bash
cd ops/compose
cp .env.example .env
docker compose up -d
```

## Status Feed
Export a local JSON feed for the Trust Center block to consume:

- **Default location:** `public://status/system.json`
- **Override via env:** `HEADY_STATUS_FEED_PATH=/absolute/path/to/system.json`

Schema reference: `docs/ops/schemas/status_feed.schema.json`.

Recommended JSON shape:
```json
{
  "status": "ok",
  "summary": "All systems operational",
  "updated_at": "2026-04-01T00:00:00Z"
}
```

## Suggested Workflow
1. Configure monitors in Uptime Kuma.
2. Publish or export a status JSON file on the Drupal host.
3. Ensure the Trust Center block can read the JSON file locally.
4. Record updates in an audit log when status changes.

## Validation
Run the local validator against the example file:

```bash
make status-feed-validate
```

## Security Notes
- Keep the status feed local to avoid exposing internal data.
- Avoid storing secrets in the JSON output.
- Gate external access through edge UI or signed requests.
