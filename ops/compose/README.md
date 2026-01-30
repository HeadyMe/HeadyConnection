# Ops Compose Stack

This directory contains docker-compose scaffolding for operations tooling.

## Uptime Kuma

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```
2. Start the stack:
   ```bash
   docker compose up -d
   ```
3. Visit `http://localhost:3001` and configure monitors.

### Status Feed
Export a local JSON status file for the Trust Center block to consume. See `docs/ops/UPTIME_KUMA.md` for the expected JSON shape, and `ops/compose/status/system.json.example` for a template.
