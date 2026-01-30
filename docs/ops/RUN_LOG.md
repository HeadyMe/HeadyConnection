# Run Log (Significant Improvements)

## IMP-20260406-22 — HeadyKinetic Deterministic Timestamp Option
- **What changed:** Added a `--timestamp` override for HeadyKinetic reports to enable deterministic outputs. (apps/heady_kinetic/kinetic_governance.py, apps/heady_kinetic/README.md)
- **Why:** Supports reproducible audit artifacts and deterministic replays.
- **Risk:** Low (optional flag).
- **Rollback:** Remove the timestamp option and revert README example.
- **Validation:** `python3 apps/heady_kinetic/kinetic_governance.py --demo`

## IMP-20260406-23 — PoPS Oracle Schema + Sample Payload
- **What changed:** Added a canonical JSON schema and sample payload for PoPS oracle ingestion. (crypto/pops_oracle/schema.json, crypto/pops_oracle/sample_payload.json)
- **Why:** Establishes a deterministic contract for telemetry ingestion.
- **Risk:** Low (additive files).
- **Rollback:** Remove the schema/sample files.
- **Validation:** `python3 scripts/crypto/validate_pops_oracle.py crypto/pops_oracle/sample_payload.json`

## IMP-20260406-24 — PoPS Oracle Validator + Makefile Target
- **What changed:** Added a PoPS oracle payload validator and Makefile target. (scripts/crypto/validate_pops_oracle.py, Makefile)
- **Why:** Enables repeatable validation for PoPS telemetry.
- **Risk:** Low (tooling only).
- **Rollback:** Remove the validator and Makefile entry.
- **Validation:** `make pops-oracle-validate`

## IMP-20260406-25 — PoPS Oracle Documentation + Nav
- **What changed:** Added PoPS Oracle docs and linked them in docs index and MkDocs nav. (docs/crypto/POPS_ORACLE.md, docs/INDEX.md, mkdocs.yml)
- **Why:** Provides accurate usage guidance and discoverability.
- **Risk:** Low (docs only).
- **Rollback:** Remove the new doc and nav links.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-26 — SPIRE Workload Registration Parameters
- **What changed:** Made SPIRE workload registration script accept env overrides for SPIFFE ID and selectors, and documented usage. (ops/spire/register_workloads.sh, ops/spire/README.md)
- **Why:** Improves operability and reduces placeholder misuse.
- **Risk:** Low (script output only).
- **Rollback:** Revert the script and README updates.
- **Validation:** `bash ops/spire/register_workloads.sh`

## IMP-20260406-27 — PoPS Oracle IP Integration Mapping
- **What changed:** Added PoPS Oracle Integrity Gate to the IP integration map. (docs/ops/IP_INTEGRATION.md)
- **Why:** Connects the new telemetry integrity concept to concrete repo components.
- **Risk:** Low (docs only).
- **Rollback:** Remove the new IP integration entry.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-28 — PoPS Oracle Invention Disclosure
- **What changed:** Added an invention disclosure for the PoPS Oracle Integrity Gate. (docs/patents/invention_disclosures/IDF-20260406-21-pops-oracle-integrity-gate.md)
- **Why:** Captures the patentable ingestion gate concept.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the IDF and index entry.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-29 — PoPS Oracle Provisional Draft
- **What changed:** Drafted a provisional application for the PoPS Oracle Integrity Gate. (docs/patents/provisional/HS-PA-057_PoPSOracleIntegrity_2026-04-06.docx)
- **Why:** Prepares the filing for legal review.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the provisional draft and index entry.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-30 — Patent Index Updates for PoPS Oracle
- **What changed:** Updated disclosure index, provisional links, and filing queue for PoPS Oracle Integrity Gate. (docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Keeps IP tracking aligned with new artifacts.
- **Risk:** Low (docs only).
- **Rollback:** Remove the added entries.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-31 — Docs Validation Coverage for PoPS Oracle
- **What changed:** Added PoPS Oracle docs and patent files to the docs validation manifest. (scripts/docs/validate_docs.py)
- **Why:** Ensures docs and artifacts remain validated in CI.
- **Risk:** Low (validation only).
- **Rollback:** Remove required-file entries.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-12 — HeadyKinetic Demo Module
- **What changed:** Added HeadyKinetic kinetic governance demo with proof-of-state output and README usage. (apps/heady_kinetic/kinetic_governance.py, apps/heady_kinetic/README.md)
- **Why:** Provides a software anchor for thermal-based kinetic verification concepts.
- **Risk:** Low (demo module only).
- **Rollback:** Remove the HeadyKinetic module directory.
- **Validation:** `python3 apps/heady_kinetic/kinetic_governance.py --demo`

## IMP-20260406-13 — HeadyKinetic Validator + Makefile Target
- **What changed:** Added a validation script and Makefile target for HeadyKinetic. (scripts/ops/validate_heady_kinetic.py, Makefile)
- **Why:** Ensures deterministic, repeatable verification of the demo output.
- **Risk:** Low (validation only).
- **Rollback:** Remove the validator and Makefile entry.
- **Validation:** `python3 scripts/ops/validate_heady_kinetic.py`

## IMP-20260406-14 — HeadyKinetic AI Documentation + Nav
- **What changed:** Added HeadyKinetic documentation and wired it into the docs index and MkDocs nav. (docs/ai/HEADY_KINETIC.md, docs/INDEX.md, mkdocs.yml)
- **Why:** Makes the new module discoverable to operators and stakeholders.
- **Risk:** Low (docs only).
- **Rollback:** Remove the docs entry and nav links.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-15 — HeadyKinetic Ops Runbook
- **What changed:** Added an ops runbook outlining safety guidance and validation steps. (docs/ops/HEADY_KINETIC_RUNBOOK.md)
- **Why:** Provides clear operational guidance for deployment and rollback.
- **Risk:** Low (docs only).
- **Rollback:** Remove the runbook.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-16 — HeadyKinetic Hardware Integration Note
- **What changed:** Extended the HeadyGuard schematic notes to include HeadyKinetic thermal sensor taps. (docs/hardware/HEADY_GUARD_SCHEMATIC.md)
- **Why:** Aligns hardware guidance with the kinetic governance requirements.
- **Risk:** Low (docs only).
- **Rollback:** Revert the schematic notes.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-17 — HeadyKinetic IP Integration Mapping
- **What changed:** Added the HeadyKinetic Next-Gen patent entry and integration targets. (docs/ops/IP_INTEGRATION.md)
- **Why:** Connects the new patent concept to concrete repository components.
- **Risk:** Low (docs only).
- **Rollback:** Remove the IP integration entry.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-18 — HeadyKinetic Invention Disclosure
- **What changed:** Added an invention disclosure for HeadyKinetic kinetic governance. (docs/patents/invention_disclosures/IDF-20260406-20-headykinetic-kinetic-governance.md)
- **Why:** Captures the patentable concept for governance workflows.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the IDF file and index entry.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-19 — HeadyKinetic Provisional Draft
- **What changed:** Drafted a provisional application for HeadyKinetic. (docs/patents/provisional/HS-PA-056_HeadyKinetic_2026-04-06.docx)
- **Why:** Prepares the Next-Gen patent for legal review.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the provisional draft and index entry.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-20 — Patent Index Updates for HeadyKinetic
- **What changed:** Updated invention disclosure index, provisional links, and filing queue to include HeadyKinetic. (docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Keeps governance tracking aligned with new IP artifacts.
- **Risk:** Low (docs only).
- **Rollback:** Remove the added entries.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-21 — Docs Validation Coverage for HeadyKinetic
- **What changed:** Added HeadyKinetic docs and runbook to the docs validation manifest. (scripts/docs/validate_docs.py)
- **Why:** Ensures docs and nav entries stay valid in CI.
- **Risk:** Low (validation only).
- **Rollback:** Remove the required-file entries.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-01 — HeadyMake JSON Input/Output Support
- **What changed:** Added JSON input parsing and output file support for Proof-of-Structure attestations, plus updated README usage. (apps/heady_make/proof_of_structure.py, apps/heady_make/README.md)
- **Why:** Enables deterministic replays and integration with upstream scanning pipelines.
- **Risk:** Low (additive CLI options).
- **Rollback:** Revert the CLI changes and README updates.
- **Validation:** `python3 apps/heady_make/proof_of_structure.py --demo`

## IMP-20260406-02 — HeadyField Oracle Payload Support
- **What changed:** Added telemetry input/output handling for the Regenerative Oracle demo and updated usage docs. (apps/heady_field/regenerative_oracle.py, apps/heady_field/README.md)
- **Why:** Allows replayable telemetry scoring and downstream audit logging.
- **Risk:** Low (additive CLI options).
- **Rollback:** Revert the CLI changes and README updates.
- **Validation:** `python3 apps/heady_field/regenerative_oracle.py --demo`

## IMP-20260406-03 — HeadyLegacy Succession Request Support
- **What changed:** Added JSON request ingestion with optional evaluation timestamp and output file support for succession checks. (apps/heady_legacy/sovereign_succession.py, apps/heady_legacy/README.md)
- **Why:** Enables deterministic governance reviews and reproducible succession eligibility checks.
- **Risk:** Low (additive CLI options).
- **Rollback:** Revert the CLI changes and README updates.
- **Validation:** `python3 apps/heady_legacy/sovereign_succession.py --demo`

## IMP-20260406-04 — Branch Consolidation Orchestrator + Runbook
- **What changed:** Added branch consolidation planner/executor script and ops runbook, plus Makefile target. (scripts/dev/branch_consolidate.py, docs/ops/BRANCH_CONSOLIDATION.md, Makefile)
- **Why:** Provides an auditable, risk-aware workflow for combining three branches safely.
- **Risk:** Medium (merge automation; can be misused without review).
- **Rollback:** Delete the consolidation branch and revert the script/runbook.
- **Validation:** `python3 scripts/dev/branch_consolidate.py --repo . --branches work --allow-single`

## IMP-20260406-05 — Status Feed Validation Hardening
- **What changed:** Extended status feed validation to enforce component schemas and timestamps. (scripts/ops/validate_status_feed.py)
- **Why:** Prevents malformed component status entries from slipping into trust-center feeds.
- **Risk:** Low (validation only).
- **Rollback:** Revert validator changes.
- **Validation:** `python3 scripts/ops/validate_status_feed.py ops/compose/status/system.json.example`

## IMP-20260406-06 — Receipt Ledger Validation
- **What changed:** Added receipts JSONL validator and documented the check in receipts runbook. (scripts/ops/validate_receipts.py, ops/receipts/README.md, Makefile)
- **Why:** Ensures receipt entries remain structurally valid and auditable.
- **Risk:** Low (validation only).
- **Rollback:** Remove the validator and revert README.
- **Validation:** `python3 scripts/ops/validate_receipts.py ops/receipts/receipts.jsonl`

## IMP-20260406-07 — Patent Index Integrity Validation
- **What changed:** Added a validator that ensures all IDFs and provisional filings are indexed. (scripts/patents/validate_patent_index.py, Makefile)
- **Why:** Prevents IP artifacts from falling out of governance tracking.
- **Risk:** Low (validation only).
- **Rollback:** Remove the validator and revert Makefile.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260406-08 — MkDocs Navigation Validation
- **What changed:** Added mkdocs nav link validation to docs checks. (scripts/docs/validate_docs.py)
- **Why:** Prevents broken docs navigation from shipping.
- **Risk:** Low (validation only).
- **Rollback:** Revert mkdocs validation logic.
- **Validation:** `python3 scripts/docs/validate_docs.py`

## IMP-20260406-09 — Admin UI OpenAPI Contract Check
- **What changed:** Validates required OpenAPI paths for the Admin UI backend. (scripts/web/validate_heady_admin_ui.py)
- **Why:** Ensures API scaffolding stays aligned with UI expectations.
- **Risk:** Low (validation only).
- **Rollback:** Revert validation logic.
- **Validation:** `python3 scripts/web/validate_heady_admin_ui.py`

## IMP-20260406-10 — Localhost Binding Hardening for Compose
- **What changed:** Bound the conductor port to localhost by default and documented the policy update. (docker-compose.yml, docs/ops/LOCALHOST_BINDING.md)
- **Why:** Reduces unintended network exposure for local deployments.
- **Risk:** Medium (remote access to the conductor now requires explicit port rebinds).
- **Rollback:** Restore the original port mapping.
- **Validation:** `python3 scripts/ops/validate_status_feed.py ops/compose/status/system.json.example`

## IMP-20260406-11 — Branch Consolidation Orchestrator IP Drafts
- **What changed:** Drafted an invention disclosure and provisional application for the branch consolidation orchestration workflow. (docs/patents/invention_disclosures/IDF-20260406-19-branch-consolidation-orchestrator.md, docs/patents/provisional/HS-PA-055_BranchConsolidationOrchestrator_2026-04-06.docx, docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Captures patentable governance automation for multi-branch consolidation.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the IDF/provisional files and update the indexes.
- **Validation:** `python3 scripts/patents/validate_patent_index.py`

## IMP-20260401-01 — Trust Narrative Manifesto and Messaging
- **What changed:** Added a consolidated manifesto, homepage hero copy, and investor summary for the trust narrative. (docs/business/TRUST_NARRATIVE.md)
- **Why:** Aligns marketing and investor materials with the proof-based trust architecture.
- **Risk:** Low (documentation only).
- **Rollback:** Revert the new doc and remove nav entries.
- **Validation:** `make docs-validate`

## IMP-20260401-02 — Documentation Navigation Updates
- **What changed:** Added Trust Narrative to docs index and MkDocs navigation.
- **Why:** Ensures content is discoverable for business and investor audiences.
- **Risk:** Low (navigation only).
- **Rollback:** Remove the nav entries.
- **Validation:** `make docs-validate`

## IMP-20260401-03 — Status Feed Schema + Example Payload
- **What changed:** Added JSON schema for status feeds and a concrete example payload.
- **Why:** Provides a consistent, validated contract for Trust Center and edge UI status.
- **Risk:** Low (additive files).
- **Rollback:** Remove schema/example and revert docs.
- **Validation:** `python3 scripts/ops/validate_status_feed.py ops/compose/status/system.json.example`

## IMP-20260401-04 — Status Feed Validator + Makefile Target
- **What changed:** Added a validator script and Makefile target to verify status feed payloads.
- **Why:** Enables repeatable local/CI validation for ops status feeds.
- **Risk:** Low (additive tooling).
- **Rollback:** Remove script and Makefile target.
- **Validation:** `make status-feed-validate`

## IMP-20260401-05 — Trust Center Status Block Hardening
- **What changed:** Added status validation, logging, and safer defaults to the Trust Center status block.
- **Why:** Improves resilience when the status feed is missing or malformed.
- **Risk:** Low (defaults to safe "unknown" state).
- **Rollback:** Revert block logic to previous simple rendering.
- **Validation:** `make docs-validate`

## IMP-20260401-06 — Edge UI Status Rendering Improvements
- **What changed:** Edge UI worker now renders summary and updated time with clearer status mappings.
- **Why:** Provides clearer, user-friendly status visibility at the edge.
- **Risk:** Low (presentation only).
- **Rollback:** Revert worker template to previous minimal output.
- **Validation:** `make docs-validate`

## IMP-20260401-07 — Uptime Kuma Ops Guidance Enhancements
- **What changed:** Added schema references and validation guidance to ops docs.
- **Why:** Reduces misconfiguration risk for status feeds.
- **Risk:** Low (docs).
- **Rollback:** Revert doc updates.
- **Validation:** `make docs-validate`

## IMP-20260401-08 — Trust Status Feed Guidance in Trust Module
- **What changed:** Documented schema and validation commands in the Trust Center module README.
- **Why:** Improves operability for Drupal administrators.
- **Risk:** Low (docs).
- **Rollback:** Revert README updates.
- **Validation:** `make docs-validate`

## IMP-20260401-09 — Trust-Layer Proof Pipeline IDF
- **What changed:** Drafted an invention disclosure describing a proof-backed status feed pipeline.
- **Why:** Captures patentable elements discovered in this run.
- **Risk:** Low (documentation).
- **Rollback:** Remove the IDF entry.
- **Validation:** `make docs-validate`

## IMP-20260401-10 — Provisional Draft for Trust-Layer Proof Pipeline
- **What changed:** Created a provisional DOCX draft and updated patent indexes/filing queue.
- **Why:** Satisfies IP capture requirements for strong invention candidates.
- **Risk:** Low (documentation).
- **Rollback:** Remove the DOCX and revert index updates.
- **Validation:** `make docs-validate`

## IMP-20260402-01 — HeadyLens Demo Scaffold
- **What changed:** Added HeadyLens demo HTML, CSS, and Three.js entrypoint with a full-body model placeholder and HUD overlay. (web/heady_lens/index.html, web/heady_lens/main.js, web/heady_lens/style.css)
- **Why:** Delivers the interactive HeadyLens demo requested by stakeholders.
- **Risk:** Low (new demo only).
- **Rollback:** Remove the `web/heady_lens/` directory.
- **Validation:** `make heady-lens-validate`

## IMP-20260402-02 — Body Part Data Store
- **What changed:** Added body part metadata with logic and IP mappings that include assignment language. (web/heady_lens/data/bodyParts.json)
- **Why:** Ensures the demo surfaces patent assignments clearly.
- **Risk:** Low (static data).
- **Rollback:** Revert the JSON file.
- **Validation:** `make heady-lens-validate`

## IMP-20260402-03 — Modular Interaction Layers
- **What changed:** Added modular loader, interaction, overlay, and data store utilities for HeadyLens. (web/heady_lens/js/*)
- **Why:** Keeps the demo maintainable and easy to extend.
- **Risk:** Low (demo-only code).
- **Rollback:** Revert the JS module files.
- **Validation:** `make heady-lens-validate`

## IMP-20260402-04 — HeadyLens Documentation
- **What changed:** Added HeadyLens README and docs page with run instructions and accessibility notes. (web/heady_lens/README.md, docs/ai/HEADY_LENS.md)
- **Why:** Provides clear instructions for local demos and docs navigation.
- **Risk:** Low (documentation).
- **Rollback:** Remove the docs entries.
- **Validation:** `make docs-validate`

## IMP-20260402-05 — HeadyLens Validator + Makefile Target
- **What changed:** Added a validation script and Makefile target for the demo. (scripts/web/validate_heady_lens.py, Makefile)
- **Why:** Makes the demo verifiable in CI/local workflows.
- **Risk:** Low (tooling only).
- **Rollback:** Remove the script and Makefile target.
- **Validation:** `make heady-lens-validate`

## IMP-20260402-06 — Patent Assignment Clarifications (Docs)
- **What changed:** Updated patent references to include assignment to HeadySystems Inc. across IP integration and trust narrative docs. (docs/ops/IP_INTEGRATION.md, docs/business/TRUST_NARRATIVE.md, docs/ai/HEADY_KAIZEN.md, docs/ai/HEADY_SYSTEMS_CORE.md)
- **Why:** Ensures patent ownership statements are explicit and consistent.
- **Risk:** Low (documentation).
- **Rollback:** Revert the doc edits.
- **Validation:** `make docs-validate`

## IMP-20260402-07 — Living Federation Assignment Updates
- **What changed:** Updated Living Federation copy and patent data to include assignment language and display it in the UI. (web/living_federation/index.html, web/living_federation/README.md, web/living_federation/data/patents.json, web/living_federation/app.js)
- **Why:** Removes ambiguous ownership statements in the demo.
- **Risk:** Low (UI/data only).
- **Rollback:** Revert the Living Federation files.
- **Validation:** `make docs-validate`

## IMP-20260402-08 — Builder Template Assignment Alignment
- **What changed:** Updated builder performance docs templates to include patent assignment language. (build_heady_drupal_project_v6_4_0_integrated_headyreflect_docs_guardian_compose_perf.py)
- **Why:** Ensures future generated repos inherit correct ownership statements.
- **Risk:** Low (template text only).
- **Rollback:** Revert the builder template changes.
- **Validation:** `make docs-validate`

## IMP-20260402-09 — HeadyLens Invention Disclosure
- **What changed:** Added an IDF draft for the HeadyLens interactive body mapping. (docs/patents/invention_disclosures/IDF-20260402-14-heady-lens-body-map.md)
- **Why:** Captures a new patentable concept discovered during demo work.
- **Risk:** Low (documentation).
- **Rollback:** Remove the IDF entry.
- **Validation:** `make docs-validate`

## IMP-20260402-10 — HeadyLens Provisional Draft + Index Updates
- **What changed:** Added a provisional DOCX and updated patent indexes/filing queue. (docs/patents/provisional/HS-PA-050_HeadyLensBodyMap_2026-04-02.docx, docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Satisfies IP capture requirements for strong invention candidates.
- **Risk:** Low (documentation).
- **Rollback:** Remove the DOCX and revert index updates.
- **Validation:** `make docs-validate`

## IMP-20260403-01 — HeadyLens glTF Asset + Expanded Body Parts
- **What changed:** Added a bundled glTF asset and expanded body part metadata for additional interactive regions. (web/heady_lens/assets/body.gltf, web/heady_lens/data/bodyParts.json, web/heady_lens/index.html)
- **Why:** Provides a richer demo model and more IP-mapped regions.
- **Risk:** Low (demo-only assets).
- **Rollback:** Remove the glTF asset and revert body-part data/controls.
- **Validation:** `make heady-lens-validate`

## IMP-20260403-02 — HeadyLens Async Loader Wiring
- **What changed:** Added async model loading with fallback logic and updated interaction wiring. (web/heady_lens/main.js, web/heady_lens/js/modelLoader.js, web/heady_lens/js/interaction.js)
- **Why:** Ensures glTF loading does not block the UI and keeps interactions consistent.
- **Risk:** Low (demo-only logic).
- **Rollback:** Revert to synchronous primitive model.
- **Validation:** `make heady-lens-validate`

## IMP-20260403-03 — Admin API Scaffold
- **What changed:** Added Express API with auth, CRUD endpoints, audit logging, and OpenAPI spec. (apps/heady_admin_ui/backend/*)
- **Why:** Provides backend foundation for the personal admin UI.
- **Risk:** Medium (in-memory storage only).
- **Rollback:** Remove backend scaffold.
- **Validation:** `python3 scripts/web/validate_heady_admin_ui.py`

## IMP-20260403-04 — Admin UI Frontend Shell
- **What changed:** Added React UI shell with dashboard, control panel, and module navigation. (apps/heady_admin_ui/frontend/src/*)
- **Why:** Establishes a usable frontend structure for the all-in-one dashboard.
- **Risk:** Low (UI scaffold).
- **Rollback:** Remove frontend scaffold.
- **Validation:** `python3 scripts/web/validate_heady_admin_ui.py`

## IMP-20260403-05 — Admin UI Build Config + Styles
- **What changed:** Added Vite config, entrypoints, and styling for responsive layout. (apps/heady_admin_ui/frontend/*)
- **Why:** Enables consistent build/dev workflow.
- **Risk:** Low.
- **Rollback:** Remove frontend build files.
- **Validation:** `python3 scripts/web/validate_heady_admin_ui.py`

## IMP-20260403-06 — Admin UI Docs + Deployment Compose
- **What changed:** Added README, architecture notes, and docker-compose scaffold. (apps/heady_admin_ui/README.md, apps/heady_admin_ui/docs/ARCHITECTURE.md, apps/heady_admin_ui/docker-compose.yml, docs/ops/ADMIN_UI.md)
- **Why:** Provides runbooks and deployment guidance.
- **Risk:** Low.
- **Rollback:** Remove documentation and compose file.
- **Validation:** `make admin-ui-validate`

## IMP-20260403-07 — Admin UI Validation Tooling
- **What changed:** Added validation scripts and Makefile target. (scripts/web/validate_heady_admin_ui.py, Makefile, apps/heady_admin_ui/scripts/*)
- **Why:** Ensures structure and API coverage can be verified.
- **Risk:** Low.
- **Rollback:** Remove validation tooling.
- **Validation:** `make admin-ui-validate`

## IMP-20260403-08 — Patent Assignment Summary + Next-Gen Clarifications
- **What changed:** Added patent assignment summary and clarified Next-Gen assignments in IP integration doc. (docs/patents/ASSIGNMENTS.md, docs/ops/IP_INTEGRATION.md)
- **Why:** Keeps patent ownership explicit and consistent.
- **Risk:** Low.
- **Rollback:** Revert assignment edits.
- **Validation:** `make docs-validate`

## IMP-20260403-09 — Change Receipt Signing
- **What changed:** Added receipt signing script and documentation for cryptographic change receipts. (scripts/ops/record_receipt.py, ops/receipts/README.md, ops/receipts/receipts.jsonl)
- **Why:** Satisfies PromptOps receipt requirements.
- **Risk:** Low (uses ephemeral keys).
- **Rollback:** Remove receipt tooling.
- **Validation:** `make docs-validate`

## IMP-20260403-10 — Admin UI Indexing
- **What changed:** Added Admin UI documentation to docs navigation and validation list. (docs/INDEX.md, mkdocs.yml, scripts/docs/validate_docs.py)
- **Why:** Ensures docs visibility and validation.
- **Risk:** Low.
- **Rollback:** Remove nav entries.
- **Validation:** `make docs-validate`

## IMP-20260404-01 — Builder Security Baselines
- **What changed:** Added secrets scanning config, dependency allowlist enforcement, MFA attestation workflow, and security validation scripts for generated repos. (scripts/security/scan_secrets.sh, scripts/security/validate_dependency_allowlist.py, scripts/security/validate_mfa_attestation.py, ops/dependency_allowlist.json, .gitleaks.toml, .security/mfa_attestation.json.example, docs/ops/MFA_REQUIREMENTS.md)
- **Why:** Establishes enforceable security guardrails for secrets, dependency drift, and access hardening.
- **Risk:** Low (additive tooling).
- **Rollback:** Remove the new security scripts and policy files.
- **Validation:** `make secrets-scan`, `make deps-allowlist-validate`, `make mfa-validate`

## IMP-20260404-02 — MCP Gateway JWT Rotation + Rate Limits
- **What changed:** Added HS256 key rotation, per-tool rate limits, and concurrency caps to the MCP gateway config and runtime. (ai/mcp-gateway/src/index.ts, ai/mcp-gateway/mcp.config.json, ai/mcp-gateway/.env.example)
- **Why:** Improves authentication resilience and protects upstream services from abuse.
- **Risk:** Medium (auth and throttling changes).
- **Rollback:** Revert MCP gateway config and runtime changes.
- **Validation:** `cd ai/mcp-gateway && npm run typecheck`

## IMP-20260404-03 — MCP Gateway Metrics + Observability Assets
- **What changed:** Added Prometheus metrics endpoint, trace context propagation, alert rules, and Grafana dashboard provisioning. (ai/mcp-gateway/src/index.ts, ops/compose/observe/prometheus.yml, ops/compose/observe/alert_rules.yml, ops/compose/observe/grafana/provisioning/dashboards/*)
- **Why:** Provides dashboards and alerting for gateway latency/error rates.
- **Risk:** Low (observability-only).
- **Rollback:** Remove observability assets and metrics endpoint.
- **Validation:** `curl http://127.0.0.1:8787/metrics`

## IMP-20260404-04 — Nginx Hardening + Performance Headers
- **What changed:** Hardened Nginx templates with CSP, HSTS, permission policies, gzip compression, and cache-control headers. (ops/compose/nginx/templates/site.conf.template, ops/baremetal/nginx/drupal_common.conf, ops/baremetal/nginx/*.conf.example)
- **Why:** Improves security posture and front-end performance by default.
- **Risk:** Medium (headers may require tuning for custom assets).
- **Rollback:** Revert Nginx template changes.
- **Validation:** `nginx -t`

## IMP-20260404-05 — Health + Readiness Endpoints
- **What changed:** Added health/readiness endpoints to Nginx templates and MCP gateway (`/healthz`, `/readyz`). (ops/compose/nginx/templates/site.conf.template, ops/baremetal/nginx/drupal_common.conf, ai/mcp-gateway/src/index.ts)
- **Why:** Enables liveness and readiness probes for orchestration and monitoring.
- **Risk:** Low.
- **Rollback:** Remove the added endpoints.
- **Validation:** `curl -f http://127.0.0.1:8787/readyz`

## IMP-20260404-06 — Reliability Runbooks
- **What changed:** Added backup/restore, disaster recovery, and cluster scale-out runbooks. (ops/runbooks/*)
- **Why:** Ensures operators have clear recovery procedures.
- **Risk:** Low (documentation).
- **Rollback:** Remove runbook files.
- **Validation:** `make docs-validate`

## IMP-20260404-07 — SLO Definitions + Overview
- **What changed:** Added SLO YAML definitions and an overview doc. (ops/slo/slo.yaml, docs/ops/SLO_OVERVIEW.md)
- **Why:** Establishes reliability targets and documentation for operators.
- **Risk:** Low.
- **Rollback:** Remove SLO definitions.
- **Validation:** `make docs-validate`

## IMP-20260404-08 — DX + Compliance Docs
- **What changed:** Added onboarding, API style guide, and release notes template docs. (docs/ops/ONBOARDING.md, docs/ops/API_STYLE_GUIDE.md, docs/ops/RELEASE_NOTES_TEMPLATE.md)
- **Why:** Improves developer onboarding and standardizes API practices.
- **Risk:** Low (documentation).
- **Rollback:** Remove the new docs.
- **Validation:** `make docs-validate`

## IMP-20260404-09 — Linting Configuration + Script
- **What changed:** Added ESLint, Markdownlint, PHPStan configs and a lint runner script. (scripts/lint/run_lints.sh, .eslintrc.cjs, .markdownlint.json, phpstan.neon)
- **Why:** Establishes consistent linting across JS, Markdown, and PHP.
- **Risk:** Low.
- **Rollback:** Remove linting configs and script.
- **Validation:** `make lint`

## IMP-20260404-10 — Autoscaling Guardrails + Cache Tuning Notes
- **What changed:** Added autoscaling guardrails doc and cache tuning guidance in Drupal settings. (docs/ops/AUTOSCALING_GUARDRAILS.md, ops/compose/drupal/settings.env.php.example)
- **Why:** Documents safe scaling limits and cache tuning hooks.
- **Risk:** Low.
- **Rollback:** Revert autoscaling doc and settings notes.
- **Validation:** `make docs-validate`

## IMP-20260404-11 — Governed Builder Guardrails Patent Draft
- **What changed:** Added invention disclosure and provisional draft for the governed builder guardrails mesh. (docs/patents/invention_disclosures/IDF-20260404-15-governed-builder-guardrails.md, docs/patents/provisional/HS-PA-051_GovernedBuilderGuardrails_2026-04-04.docx, docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Captures a new patentable architecture discovered during builder hardening.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the new IDF/provisional entries and revert patent index updates.
- **Validation:** `make docs-validate`

## IMP-20260405-01 — HeadyMake/Field/Legacy Prototype Modules
- **What changed:** Added prototype modules and demo scripts for HeadyMake, HeadyField, and HeadyLegacy. (apps/heady_make/*, apps/heady_field/*, apps/heady_legacy/*)
- **Why:** Provides sample code modules for Proof-of-Structure, Regenerative Oracle, and Sovereign Succession workflows.
- **Risk:** Low (additive prototypes).
- **Rollback:** Remove the new app directories.
- **Validation:** `python3 apps/heady_make/proof_of_structure.py --demo`

## IMP-20260405-02 — HeadyMake/Field/Legacy Documentation
- **What changed:** Added module documentation and linked it in docs navigation. (docs/ai/HEADY_MAKE.md, docs/ai/HEADY_FIELD.md, docs/ai/HEADY_LEGACY.md, docs/INDEX.md, mkdocs.yml)
- **Why:** Makes the new technologies discoverable and aligned with the mission narrative.
- **Risk:** Low (documentation).
- **Rollback:** Remove the new docs and nav entries.
- **Validation:** `make docs-validate`

## IMP-20260405-03 — HeadyLens Module Hotspots
- **What changed:** Extended the HeadyLens demo with HeadyMake/Field/Legacy hotspots and overlay entries. (web/heady_lens/data/bodyParts.json, web/heady_lens/js/modelLoader.js, web/heady_lens/index.html)
- **Why:** Adds interactive demo elements for the new modules.
- **Risk:** Low (demo-only).
- **Rollback:** Revert HeadyLens demo changes.
- **Validation:** `make heady-lens-validate`

## IMP-20260405-04 — HeadyLens Validator Coverage
- **What changed:** Updated the HeadyLens validator to require the new module entries. (scripts/web/validate_heady_lens.py)
- **Why:** Ensures demo data coverage for new modules.
- **Risk:** Low.
- **Rollback:** Revert validator changes.
- **Validation:** `make heady-lens-validate`

## IMP-20260405-05 — Living Federation Modules Dashboard
- **What changed:** Added module dashboard cards, status pills, and demo actions for HeadyMake/Field/Legacy. (web/living_federation/index.html, web/living_federation/app.js)
- **Why:** Surfaces new technologies in the living federation demo UI.
- **Risk:** Low (demo-only UI).
- **Rollback:** Revert dashboard updates.
- **Validation:** `make docs-validate`

## IMP-20260405-06 — Living Federation Patent Index Expansion
- **What changed:** Added HeadyMake/Field/Legacy entries to the Living Federation patent data. (web/living_federation/data/patents.json)
- **Why:** Keeps the patent demo aligned with the new technologies.
- **Risk:** Low.
- **Rollback:** Revert patent data additions.
- **Validation:** `make docs-validate`

## IMP-20260405-07 — HeadyMake/Field/Legacy Invention Disclosures
- **What changed:** Added invention disclosures for HeadyMake, HeadyField, and HeadyLegacy. (docs/patents/invention_disclosures/IDF-20260404-16-heady-make-proof-structure.md, IDF-20260404-17-heady-field-regenerative-oracle.md, IDF-20260404-18-heady-legacy-sovereign-succession.md)
- **Why:** Captures patentable concepts for the new technologies.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the new IDFs.
- **Validation:** `make docs-validate`

## IMP-20260405-08 — HeadyMake/Field/Legacy Provisional Drafts
- **What changed:** Drafted provisional patent applications for HeadyMake, HeadyField, and HeadyLegacy. (docs/patents/provisional/HS-PA-052_HeadyMakeProofOfStructure_2026-04-04.docx, HS-PA-053_HeadyFieldRegenerativeOracle_2026-04-04.docx, HS-PA-054_HeadyLegacySovereignSuccession_2026-04-04.docx)
- **Why:** Establishes initial filings for the new patents.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the provisional drafts.
- **Validation:** `make docs-validate`

## IMP-20260405-09 — Patent Index Updates
- **What changed:** Updated patent indexes and filing queue to include new drafts. (docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md, scripts/docs/validate_docs.py)
- **Why:** Keeps the patent tracking system consistent.
- **Risk:** Low.
- **Rollback:** Revert index updates.
- **Validation:** `make docs-validate`

## IMP-20260405-10 — IP Integration Map Updates
- **What changed:** Added HeadyMake/Field/Legacy integration references. (docs/ops/IP_INTEGRATION.md)
- **Why:** Ties new patents to implementation surfaces.
- **Risk:** Low.
- **Rollback:** Revert IP integration updates.
- **Validation:** `make docs-validate`

## IMP-20260406-01 — Heady Federation Vertical Package Scaffold
- **What changed:** Added the `heady_project/src` package and vertical module namespace. (heady_project/src/__init__.py, heady_project/src/verticals/__init__.py)
- **Why:** Establishes a clean, isolated namespace for each vertical’s runtime logic.
- **Risk:** Low (new modules only).
- **Rollback:** Remove the new package files.
- **Validation:** `make heady-project-validate`

## IMP-20260406-02 — Governance + Throttle Core
- **What changed:** Implemented HeadyReflect governance records and per-vertical throttle accounting. (heady_project/src/governance.py, heady_project/src/throttle.py)
- **Why:** Enforces intent registration and usage tracking without cross-vertical data leakage.
- **Risk:** Low (new modules only).
- **Rollback:** Remove the governance and throttle modules.
- **Validation:** `make heady-project-validate`

## IMP-20260406-03 — HeadySymphony Narrative-to-MIDI Engine
- **What changed:** Added narrative-to-MIDI mapping with intent registration for realtime audio work. (heady_project/src/verticals/symphony.py)
- **Why:** Enables Symphony to execute a deterministic demo flow and request compute intent.
- **Risk:** Low (demo-only logic).
- **Rollback:** Remove the Symphony vertical module.
- **Validation:** `make heady-project-validate`

## IMP-20260406-04 — HeadyBio Ephemeral Processor
- **What changed:** Added RAM-only spooled processing with overwrite on completion. (heady_project/src/verticals/bio.py)
- **Why:** Demonstrates ephemeral handling for sensitive payloads in the Bio vertical.
- **Risk:** Low (demo-only logic).
- **Rollback:** Remove the Bio vertical module.
- **Validation:** `make heady-project-validate`

## IMP-20260406-05 — HeadyMint Token Issuer + Ledger
- **What changed:** Added φ-based reward issuance and hashed ledger entries. (heady_project/src/verticals/mint.py)
- **Why:** Simulates proof-of-revenue minting without cross-vertical state sharing.
- **Risk:** Low (demo-only logic).
- **Rollback:** Remove the Mint vertical module.
- **Validation:** `make heady-project-validate`

## IMP-20260406-06 — Federation CLI Runner
- **What changed:** Added CLI entrypoint to run vertical demos with explicit flags. (heady_project/src/main.py)
- **Why:** Provides a consistent operator surface for launching vertical workflows.
- **Risk:** Low (new entrypoint).
- **Rollback:** Remove the main CLI entrypoint.
- **Validation:** `make heady-project-validate`

## IMP-20260406-07 — Admin Console Actions
- **What changed:** Added console actions for Symphony, Bio, and Mint verticals. (heady_project/src/admin_console.py)
- **Why:** Enables admin-side orchestration of vertical runs in a controlled interface.
- **Risk:** Low (new entrypoint).
- **Rollback:** Remove the admin console entrypoint.
- **Validation:** `make heady-project-validate`

## IMP-20260406-08 — Governance Compliance Tests
- **What changed:** Added unit tests to validate governance records for each vertical. (tests/test_verticals.py)
- **Why:** Ensures every vertical emits a HeadyReflect record with intent and usage.
- **Risk:** Low (tests only).
- **Rollback:** Remove the test file.
- **Validation:** `make heady-project-validate`

## IMP-20260406-09 — Heady Project Validation Script
- **What changed:** Added validation helper and Makefile target for the vertical test suite. (scripts/ops/validate_heady_project.py, Makefile)
- **Why:** Provides a single command to validate the new vertical stack.
- **Risk:** Low (tooling only).
- **Rollback:** Remove the validation script and Makefile target.
- **Validation:** `make heady-project-validate`

## IMP-20260406-10 — Vertical Enablement Phasing Plan
- **What changed:** Documented a four-version plan to phase the vertical delivery. (docs/ops/HEADY_VERTICALS_PHASES.md)
- **Why:** Aligns the requested work split into clear release slices.
- **Risk:** Low (docs only).
- **Rollback:** Remove the plan document.
- **Validation:** `make docs-validate`

## IMP-20260406-11 — Federated Vertical Intent Ledger IDF
- **What changed:** Added an invention disclosure for federated vertical intent governance. (docs/patents/invention_disclosures/IDF-20260406-22-federated-vertical-intent-ledger.md)
- **Why:** Captures the patentable governance + deterministic output pipeline.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the IDF entry.
- **Validation:** `make docs-validate`

## IMP-20260406-12 — Federated Vertical Intent Ledger Provisional Draft
- **What changed:** Drafted a provisional application and updated patent indexes. (docs/patents/provisional/HS-PA-058_FederatedVerticalIntentLedger_2026-04-06.docx, docs/patents/INVENTION_DISCLOSURE_INDEX.md, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Establishes an initial filing package for the governance ledger concept.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the provisional draft and revert index updates.
- **Validation:** `make docs-validate`

## IMP-20260406-13 — HeadySymphony Voice Clone Core
- **What changed:** Added voice cloning orchestration with backend selection and reference hashing. (heady_music_symphony/heady-symphony/app/voice_clone.py)
- **Why:** Moves the voice cloning feature beyond a simulated placeholder.
- **Risk:** Low (new module only).
- **Rollback:** Remove the voice clone module.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-14 — Temporary Artifact Cleanup
- **What changed:** Added a temp artifact store to auto-clean cloned audio outputs. (heady_music_symphony/heady-symphony/app/voice_clone.py)
- **Why:** Prevents orphaned audio files during repeated runs.
- **Risk:** Low (new helper only).
- **Rollback:** Remove the temp artifact helper.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-15 — Voice Clone CLI
- **What changed:** Added CLI entrypoint for voice cloning with persistence controls. (heady_music_symphony/heady-symphony/app/voice_clone_cli.py)
- **Why:** Gives operators a runnable interface for the feature.
- **Risk:** Low (new CLI only).
- **Rollback:** Remove the CLI file.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-16 — Voice Clone Configuration
- **What changed:** Added environment-driven model configuration for voice cloning. (heady_music_symphony/heady-symphony/app/voice_clone_config.py, heady_music_symphony/heady-symphony/.env.example)
- **Why:** Enables model selection without code changes.
- **Risk:** Low (config only).
- **Rollback:** Remove the config helper and env example.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-17 — Voice Clone Validation Tests
- **What changed:** Added unit tests validating output creation and cleanup. (tests/test_voice_clone.py)
- **Why:** Ensures the feature is verifiable in CI/local workflows.
- **Risk:** Low (tests only).
- **Rollback:** Remove the test file.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-18 — HeadySymphony Validation Script + Makefile Target
- **What changed:** Added validation helper and Makefile target for voice cloning. (scripts/ops/validate_heady_symphony.py, Makefile)
- **Why:** Provides a single command to validate the new runtime.
- **Risk:** Low (tooling only).
- **Rollback:** Remove the validation script and Makefile target.
- **Validation:** `make heady-symphony-validate`

## IMP-20260406-19 — HeadySymphony Ops Documentation
- **What changed:** Documented voice clone usage and cleanup policy. (heady_music_symphony/heady-symphony/README.md, heady_music_symphony/heady-symphony/ops/RUNBOOK.md)
- **Why:** Ensures operators understand inputs, outputs, and cleanup behavior.
- **Risk:** Low (docs only).
- **Rollback:** Revert documentation updates.
- **Validation:** `make docs-validate`

## IMP-20260406-20 — CodeQL Workflow
- **What changed:** Added CodeQL workflow to ensure security scans execute. (.github/workflows/codeql.yml)
- **Why:** Resolves the “no jobs run” issue for CodeQL in CI.
- **Risk:** Low (CI only).
- **Rollback:** Remove the workflow file.
- **Validation:** N/A (CI workflow).

## IMP-20260406-21 — Zero-Shot Voice Clone IDF
- **What changed:** Added an invention disclosure for the voice cloning orchestrator. (docs/patents/invention_disclosures/IDF-20260406-23-zero-shot-voice-clone-orchestrator.md, docs/patents/INVENTION_DISCLOSURE_INDEX.md)
- **Why:** Captures the patentable orchestration and cleanup approach.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the IDF entry.
- **Validation:** `make docs-validate`

## IMP-20260406-22 — Zero-Shot Voice Clone Provisional Draft
- **What changed:** Drafted a provisional application and updated patent indexes. (docs/patents/provisional/HS-PA-059_ZeroShotVoiceCloneOrchestrator_2026-04-06.docx, docs/patents/PROVISIONAL_LINKS.md, docs/patents/FILING_QUEUE.md)
- **Why:** Establishes a filing package for the voice cloning pipeline.
- **Risk:** Low (documentation only).
- **Rollback:** Remove the provisional draft and revert index updates.
- **Validation:** `make docs-validate`
