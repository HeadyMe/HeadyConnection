# HeadyKaizen (Patent #8 — assigned to HeadySystems Inc.)

## Purpose
HeadyKaizen is the continuous improvement loop for the Heady ecosystem. It collects
non-sensitive metadata signals, prioritizes improvements, and tracks execution without
cross-vertical data sharing.

## Inputs
- Iteration manifest health from `heady_iterations/`.
- DocsGuardian drift signals.
- Metadata-only operational telemetry.

## Outputs
- Prioritized improvement backlog items.
- Kaizen execution status updates for dashboards (e.g., Genesis).

## Guardrails
- Metadata-only inputs; no raw payloads.
- Vertical isolation preserved; routing metadata only.

## Integration
- Genesis Dashboard consumes Kaizen backlog metadata from `web/genesis_dashboard/data/manifest.json`.

## Source Prompt
The user-provided prompt referenced `file-E9a5ioQ16ngXxiwCVXzUJ7`, which was unavailable in this
environment. Integrate additional requirements when the prompt content is available.
