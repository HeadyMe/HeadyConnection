# Iteration Scripts Runbook

## Purpose
Run the staged iteration scripts (Heady_it1-4) deterministically and validate the generated
manifests for downstream merges.

## Scripts
- `Heady_it1_v_1_0_0.py`
- `Heady_it2_v_1_0_0.py`
- `Heady_it3_v_1_0_0.py`
- `Heady_it4_v_1_0_0.py`

## Run Order
```bash
python3 Heady_it1_v_1_0_0.py
python3 Heady_it2_v_1_0_0.py
python3 Heady_it3_v_1_0_0.py
python3 Heady_it4_v_1_0_0.py
```

## Validation
```bash
python3 scripts/docs/validate_heady_iterations.py
```

## Output
`heady_iterations/it1..it4/manifest.json`

## Rollback
Delete `heady_iterations/` and re-run the scripts.
