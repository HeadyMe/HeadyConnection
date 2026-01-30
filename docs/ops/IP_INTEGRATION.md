# IP Integration Map

This document links the patent portfolio to concrete repository components where each concept can be realized.

## Governance + Safety
- **Patent 11 (AI Tool Safety Gateway — assigned to HeadySystems Inc.):** MCP gateway confirmation gate and JWT enforcement. (`ai/mcp-gateway`)
- **Patent 14 (RAA Execution Fabric — assigned to HeadySystems Inc.):** HeadyConductor registry + vertical auth scaffolds. (`heady_conductor`)
- **Patent 17 (Policy Supply Chain — assigned to HeadySystems Inc.):** governance lock + install scripts. (`governance.lock.json`, `scripts/governance/*`)
- **Patent 38 (HeadyGate — assigned to HeadySystems Inc.):** reflection-gated MCP gateway with destructive confirmation. (`ai/mcp-gateway`)
- **Patent 51 (Governed Builder Guardrails — assigned to HeadySystems Inc.):** builder-enforced security baselines, MFA attestation, and dependency allowlist gates. (`build_heady_drupal_project_v6_4_0_integrated_headyreflect_docs_guardian_compose_perf.py`, `scripts/security/*`, `ops/dependency_allowlist.json`)

## Privacy + Trust
- **Patent 16 (Tunnel-Only Origin — assigned to HeadySystems Inc.):** Cloudflare tunnel-only origin templates. (`ops/cloudflare`, `ops/systemd`)
- **Patent 19 (HeadyBio — assigned to HeadySystems Inc.):** RAM-only processing helpers. (`heady_bio/processor.py`)
- **Patent 21 (HeadyGuard — assigned to HeadySystems Inc.):** hardware schematic concept for safety limiters. (`docs/hardware/HEADY_GUARD_SCHEMATIC.md`)
- **Patent 7 (Data Sovereignty Vaults — assigned to HeadySystems Inc.):** localhost-bound origin + payload limits for sensitive data. (`ops/prod/*`, `docs/ops/HEADY_BIO_LIMITS.md`)

## Intelligence + Reflection
- **Patent 29 (HeadyReflect — assigned to HeadySystems Inc.):** reflection enforcement toggle in MCP gateway. (`ai/mcp-gateway/src/index.ts`)
- **Patent 32 (HeadyTempo — assigned to HeadySystems Inc.):** Intel Edge scheduler stub to precompute opportunities. (`ai/intel-edge/worker.js`)

## Manufacturing + Regeneration
- **Patent 35 (HeadyMake — Proof-of-Structure — assigned to HeadySystems Inc.):** layer-by-layer scan, hash, and certificate pipeline. (`apps/heady_make`, `docs/ai/HEADY_MAKE.md`)
- **Patent 36 (HeadyField — Regenerative Oracle — assigned to HeadySystems Inc.):** soil telemetry oracle and incentive gating. (`apps/heady_field`, `docs/ai/HEADY_FIELD.md`)
- **Patent 37 (HeadyLegacy — Sovereign Succession — assigned to HeadySystems Inc.):** biometric succession protocol with secret sharing. (`apps/heady_legacy`, `docs/ai/HEADY_LEGACY.md`)

## Economics + Operations
- **Patent 33 (HeadyMint — assigned to HeadySystems Inc.):** compliance-first HeadyCoin docs and Drupal module. (`docs/crypto/*`, `web/modules/custom/heady_coin`)
- **Patent 34 (HeadyPhi — assigned to HeadySystems Inc.):** deterministic scaling helper and standard. (`ops/tools/lib_heady_phi.py`, `docs/ops/HEADY_PHI_STANDARD.md`)
- **Patent 41 (HeadyFoundations — assigned to HeadySystems Inc.):** universal constants engine for constant-aligned scoring and safety gates. (`docs/ai/HEADY_SYSTEMS_CORE.md`, `ops/tools/lib_heady_phi.py`)

## New Patent 37 (HeadyNature — assigned to HeadySystems Inc.)
- Biomimetic translation node captured in the invention disclosure and provisional application.
- Future integration target: Intel Edge + Conductor orchestration for translating biological motifs into scaling policies.

## New Patent 39 (HeadyGaia — assigned to HeadySystems Inc.)
- Nature-only model training with anthropogenic exclusion aligns with Intel Edge data curation and Conductor policy enforcement.
- Future integration target: biomimetic tokenizer + evolutionary inference services in the AI stack for sustainability optimization.

## Patent 40 Placeholder (System Name TBD — assigned to HeadySystems Inc.)
- Template application staged for a new system pending naming and disclosure details.
- Future integration target: to be linked once the system name, modules, and routing constraints are defined.

## New Patent 42 (Living Federation — assigned to HeadySystems Inc.)
- Metadata-only patent operations dashboard with policy-verified demo workflows.
- Current integration target: living federation web demo + docs runbook.

## New Patent 43 (Demo Integrity Ledger — Next-Gen Patent 1 — assigned to HeadyConnection Inc.)
- Local-only ledger for demo actions and manifest validation.
- Current integration target: living federation activity log + manifest validator.

## New Patent 44 (Demo Snapshot Export — Next-Gen Patent 2 — assigned to HeadyConnection Inc.)
- Policy-aware metadata export for demo sessions.
- Current integration target: Living Federation export log action + manifest snapshot metadata.

## New Patent 45 (Manifest Integrity Gate — Next-Gen Patent 3 — assigned to HeadyConnection Inc.)
- Schema-validated manifest gating for metadata-only demos.
- Current integration target: Living Federation manifest validator + offline fallback banner.

## New Patent 46 (Iteration Pipeline Orchestrator — Next-Gen Patent 4 — assigned to HeadyConnection Inc.)
- Deterministic iteration scripts with manifest gating.
- Current integration target: Heady_it1-4 scripts + validation gate.

## New Patent 47 (HeadyKinetic — Next-Gen Patent 5 — assigned to HeadyConnection Inc.)
- Kinetic governance via distributed spectral sensing for actuator and RF thermal verification.
- Current integration target: HeadyKinetic demo module + hardware concept updates. (`apps/heady_kinetic`, `docs/ai/HEADY_KINETIC.md`, `docs/hardware/HEADY_GUARD_SCHEMATIC.md`)

## New Patent 48 (PoPS Oracle Integrity Gate — assigned to HeadySystems Inc.)
- Deterministic schema + signature validation for PoPS telemetry ingestion.
- Current integration target: PoPS oracle schema + validator + docs. (`crypto/pops_oracle`, `scripts/crypto/validate_pops_oracle.py`, `docs/crypto/POPS_ORACLE.md`)

## Patent 8 (HeadyKaizen — assigned to HeadySystems Inc.)
- Metadata-only continuous improvement loop for backlog ranking.
- Current integration target: Genesis Dashboard + iteration manifests.

> Update this map as each vertical moves from scaffold to implementation.
