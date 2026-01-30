# HeadyLens Interactive Body Demo

## Purpose
HeadyLens demonstrates how Heady systems surface internal logic and IP references through a body-like, visual interface. The demo uses a 3D model, hover/click ray-casting, and a HUD overlay to map body parts to system logic.

## Location
- `web/heady_lens/`

## Run
```bash
cd web/heady_lens
python3 -m http.server 8003
```

## Data Store
The body-part metadata lives in `web/heady_lens/data/bodyParts.json`. Sample entries include HeadyMake, HeadyField, and HeadyLegacy modules with explicit patent assignment to HeadySystems Inc.

## Model Assets
The demo attempts to load `web/heady_lens/assets/body.gltf` and falls back to a primitive-built body if the asset is unavailable.

## Accessibility
- Keyboard navigable control buttons (Enter/Space).
- `aria-live` overlay for status updates.

## Validation
```bash
make heady-lens-validate
```
