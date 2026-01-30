# Heady Genesis Dashboard

## Purpose
The Genesis Dashboard is a local-first, metadata-only UI that tracks continuous improvement
signals for HeadyKaizen and iteration pipeline health without exposing sensitive data.

## Location
`web/genesis_dashboard/`

## Run
```bash
python3 -m http.server 8080
```
Then visit `http://localhost:8080/web/genesis_dashboard/`.

## Validation
```bash
python3 scripts/docs/validate_genesis_dashboard.py
```

## Guardrails
- Local-only data sources (`data/manifest.json`).
- No cross-vertical data sharing; metadata routing only.
- CSP enforced via meta tag for static demo safety.
