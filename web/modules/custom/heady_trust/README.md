# Heady Trust Center

Provides Trust Center content and scaffolding for governance-first messaging.

## Drush
- `drush heady-trust:seed` seeds placeholder Trust Center pages and footer links.

## Notes
This module is intentionally conservative and must not expose sensitive system data. Replace stubs with approved content as part of deployment.

## System Status Feed
The status block reads a local JSON file (default: `public://status/system.json`). Override with `HEADY_STATUS_FEED_PATH` to point to a local absolute path.

Schema reference: `docs/ops/schemas/status_feed.schema.json`. Use `make status-feed-validate` to validate the example payload.
