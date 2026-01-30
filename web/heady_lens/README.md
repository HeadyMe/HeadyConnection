# HeadyLens Interactive Body Demo

This demo simulates the HeadyLens interface by mapping body parts to Heady system logic and IP references. The demo is intentionally lightweight and uses a bundled glTF mesh with a primitive fallback. Replace the generated model with a production-grade anatomical mesh as needed.

## Run Locally
```bash
cd web/heady_lens
python3 -m http.server 8003
```

Then open `http://localhost:8003` in your browser.

## Controls
- Drag to rotate the model, scroll to zoom.
- Hover a body part to highlight it.
- Click a body part or use the buttons to zoom in and display the overlay.

## Data
Body part logic and IP references live in `data/bodyParts.json`. The demo now includes HeadyMake, HeadyField, and HeadyLegacy modules, with explicit patent assignment references to HeadySystems Inc.

## Model Assets
The demo attempts to load `assets/body.gltf`. If the asset fails to load, it falls back to the primitive model.

## Accessibility
The overlay uses `aria-live="polite"` and control buttons provide keyboard activation via Enter/Space.
