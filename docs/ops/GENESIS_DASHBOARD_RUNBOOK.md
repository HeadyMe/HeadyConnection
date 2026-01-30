# Genesis Dashboard Runbook

## Purpose
Operate the Heady Genesis Dashboard locally for Kaizen and iteration visibility without
exposing sensitive data.

## Run
```bash
python3 -m http.server 8080
```
Then visit `http://localhost:8080/web/genesis_dashboard/`.

## Validation
```bash
python3 scripts/docs/validate_genesis_dashboard.py
```

## Notes
- Metadata-only manifest at `web/genesis_dashboard/data/manifest.json`.
- No cross-vertical data sharing.
