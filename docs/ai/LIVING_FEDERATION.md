# Living Federation Interactive Web System

## Purpose
The Living Federation experience is a static, local-first web interface that presents the
HeadySystems patent series (Patents 1–42 — assigned to HeadySystems Inc.) as an interactive dashboard. It emphasizes demonstrability without
exposing any sensitive or cross-vertical data. The demo is designed to work entirely offline
and can be hosted on localhost for internal stakeholder walkthroughs.

## Architecture
- **Static UI**: `web/living_federation/index.html` + `styles.css` + `app.js`.
- **Data Source**: `web/living_federation/data/manifest.json` (metadata only).
- **Runtime**: Any static server (e.g., `python3 -m http.server`).

## Interactive Components
- **Federation Status**: Simulated state cards showing governance, MCP gateway, Intel Edge, and
  DocsGuardian health.
- **Patent Index**: Filterable cards with status, integration hints, and tags.
- **Interactive Demos**: Mock actions showing how HeadyReflect, RAA Fabric, and Conductor orchestration
  could surface in a safe UI.
- **Activity Log**: Local-only log entries stored in browser storage for traceable demo sessions.
- **Snapshot Export**: Metadata-only log export bundles include policy snapshot identifiers.
- **Manifest Snapshot**: Schema version + manifest ID included for audit trails.

## Security & Compliance Guardrails
- No external dependencies or network calls beyond local JSON.
- Localhost-first usage; no public bindings by default.
- No cross-vertical data sharing; all content is non-sensitive metadata.
- Manifest validation to prevent malformed metadata from rendering.

## Runbook
```bash
python3 -m http.server 8080
```
Then visit `http://localhost:8080/web/living_federation/`.

## Validation
```bash
python3 scripts/docs/validate_living_federation.py
```

## Ops Runbook
See `docs/ops/LIVING_FEDERATION_RUNBOOK.md` for the operational checklist and rollback steps.

## Manifest Spec
See `docs/ops/LIVING_FEDERATION_MANIFEST.md` for the manifest schema and validation rules.

## Source Prompt
The user-provided prompt referenced an attached file (`file-WTqWAZ9Bb9ysqKsw9jqbcD`). The
attached content was not available in the execution environment, so this implementation follows
the high-level requirements described in the request (interactive patent dashboard, demos,
security constraints). Add the missing details when the full prompt content is available.
