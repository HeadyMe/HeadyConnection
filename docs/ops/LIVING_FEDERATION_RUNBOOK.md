# Living Federation Demo Runbook

## Purpose
Provide a repeatable, local-first way to run the Living Federation demo without exposing sensitive
systems or violating vertical isolation requirements.

## Prerequisites
- Python 3.x installed locally.
- No external network dependencies required.

## Start the demo
```bash
python3 -m http.server 8080
```
Then open: `http://localhost:8080/web/living_federation/`.

## Validation Steps
1. Confirm the **Federation Status** cards render.
2. Search the **Patent Index** to verify filtering works.
3. Click demo actions to ensure entries appear in the **Activity Log**.
4. Check that no external network requests appear in browser dev tools (only local `patents.json`).
5. Confirm the Policy Snapshot card reflects `manifest.json` metadata.
6. Export the log and confirm the JSON includes `snapshot` metadata.
7. Confirm manifest schema version and manifest ID are visible in the Policy Snapshot panel.

## Security Notes
- Static assets only, no remote API calls.
- Localhost-only by default.
- Activity logs stored in localStorage.

## Rollback
If issues occur, revert the Living Federation demo folder and remove references from docs nav and
DocsGuardian required files list.
