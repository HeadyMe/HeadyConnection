# Living Federation Manifest Specification

## Purpose
Define the metadata manifest consumed by the Living Federation demo to ensure deterministic
rendering and policy snapshot traceability.

## File Location
`web/living_federation/data/manifest.json`

## Schema
```json
{
  "snapshot": {
    "version": "policy-pack-1.3.2",
    "generated_at": "2026-01-22T00:00:00Z",
    "source": "docs-guardian",
    "schema_version": "1.0.0",
    "manifest_id": "lf-demo-0001"
  },
  "patents": [
    {
      "number": "13",
      "title": "Deterministic Repo Builder",
      "status": "Operational",
      "summary": "...",
      "integration": "...",
      "tags": ["determinism", "build"]
    }
  ]
}
```

## Required Fields
- **snapshot.version**: policy snapshot or bundle identifier.
- **snapshot.generated_at**: ISO-8601 timestamp for when the manifest was generated.
- **snapshot.source**: system identifier producing the manifest.
- **snapshot.schema_version**: manifest schema version for validation.
- **snapshot.manifest_id**: stable manifest identifier for audit trails.
- **patents**: array of patent entries with required fields:
  - `number`, `title`, `status`, `summary`, `integration`, `tags` (array).

## Validation
Run:
```bash
python3 scripts/docs/validate_living_federation.py
```

## Notes
- Keep content metadata-only. Do not embed sensitive payloads.
- The demo falls back to static metadata if the manifest is unavailable.
- Legacy fallback: `data/patents.json` is still supported for compatibility.
