# Iteration Scripts Prompt (Interim Operating Notes)

The original attachment describing the four iteration scripts is still unavailable in this
environment. The guidance below captures the current operating procedure so the iteration outputs
can be merged deterministically while we wait for the canonical prompt content.

## Required Follow-up
1. Add the full prompt content from the attachment (`file-6mDqdXUbp2VibmaZN3SG5V`) to this file.
2. Confirm script names, paths, and expected outputs against the attachment.
3. Document merge order and any conflict resolution guidance from the original prompt.

## Iteration Script Inventory
- `./Heady_it1_v_1_0_0.py` writes `heady_iterations/it1/manifest.json`.
- `./Heady_it2_v_1_0_0.py` writes `heady_iterations/it2/manifest.json`.
- `./Heady_it3_v_1_0_0.py` writes `heady_iterations/it3/manifest.json`.
- `./Heady_it4_v_1_0_0.py` writes `heady_iterations/it4/manifest.json`.

## Context-Dump Merge Tooling
Use `scripts/ops/merge_context_dumps.py` to consolidate iteration manifests into a single release
context dump.

Example (default manifests):
```
python3 scripts/ops/merge_context_dumps.py
```

Example (explicit manifests + placeholder resolution + IP capture):
```
python3 scripts/ops/merge_context_dumps.py \
  --inputs heady_iterations/it1/manifest.json heady_iterations/it2/manifest.json \
  --placeholder PLACEHOLDER=resolved-value \
  --ip-artifact docs/patents/invention_disclosures/IDF-20260402-14-heady-lens-body-map.md \
  --ip-note "Captured HeadyLens body-map disclosure for merge context."
```

## Placeholder Resolution Guidance
- Resolve placeholder tokens (e.g., `PLACEHOLDER`, `REPLACE`, `TBD`) using `--placeholder TOKEN=VALUE`.
- The merge tool fails by default if placeholder tokens remain; pass `--allow-placeholders` only for
  draft merges.

## IP Capture Guidance
- Provide invention disclosures, provisional drafts, or other IP-sensitive artifacts via
  `--ip-artifact` so the merge output records hashes and timestamps.
- Keep IP capture notes concise and aligned with the artifact being referenced.

## Validation
Once the attachment is available, add the complete script execution commands and validation checks
from the canonical prompt here.
