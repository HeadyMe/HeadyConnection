# HeadyMusic + HeadySymphony Scaffold Generator

## Purpose
This script builds a deterministic skeleton for the HeadyMusic and HeadySymphony repos, keeping
all data isolation constraints intact and providing a base for mobile/web integrations.

## Script
- `HeadyMusic_HeadySymphony_v_1_0_0.py`

## Output
The script writes to `heady_music_symphony/` with two repos:
- `heady-music/`
- `heady-symphony/`

Each repo contains `app/`, `docs/`, `ops/`, and `scripts/` directories plus baseline README and
runbook content.

## Run
```bash
python3 HeadyMusic_HeadySymphony_v_1_0_0.py
```

## Data Isolation Notes
Ensure audio processing and metadata pipelines stay isolated per vertical. Only non-sensitive
routing metadata should be shared between services.
