# Living Federation Web Demo

This static web experience demonstrates the HeadySystems patent series (Patents 1–42 — assigned to HeadySystems Inc.) with
interactive dashboards, patent summaries, and controlled demos. It intentionally avoids any
sensitive data or cross-vertical interactions.

## Manifest
The demo loads metadata from `data/manifest.json` and falls back to `data/patents.json` if needed.
The manifest includes schema version and manifest ID for audit trails.

## Activity Log
The demo records local-only activity entries and allows exporting a metadata-only JSON summary.

## Run locally
```bash
python3 -m http.server 8080
```
Open `http://localhost:8080/web/living_federation/`.

## Security notes
- Static assets only; no API calls beyond local JSON.
- No cross-vertical data exchange (metadata routing concepts only).
- Designed for localhost-first deployment.
