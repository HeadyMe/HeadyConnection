#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

REQUIRED_FILES = [
    "docs/INDEX.md",
    "docs/ai/INTEL_EDGE.md",
    "docs/ai/HEADY_REFLECT.md",
    "docs/ai/MCP_GATEWAY.md",
    "docs/ai/HEADY_SYSTEMS_CORE.md",
    "docs/ai/LIVING_FEDERATION.md",
    "docs/ai/HEADY_LENS.md",
    "docs/ai/HEADY_MAKE.md",
    "docs/ai/HEADY_FIELD.md",
    "docs/ai/HEADY_LEGACY.md",
    "docs/ai/HEADY_KINETIC.md",
    "docs/ai/HEADY_MUSIC_SYMPHONY.md",
    "docs/ai/HEADY_GENESIS_DASHBOARD.md",
    "docs/ai/HEADY_KAIZEN.md",
    "docs/crypto/OVERVIEW.md",
    "docs/crypto/WHITEPAPER_DRAFT.md",
    "docs/crypto/TOKENOMICS.md",
    "docs/crypto/POPS_PROTOCOL.md",
    "docs/crypto/POPS_ORACLE.md",
    "docs/crypto/COMPLIANCE.md",
    "docs/crypto/LAUNCH_CHECKLIST.md",
    "docs/crypto/SECURITY.md",
    "docs/ops/POST_GENERATION_NOTES.md",
    "docs/ops/IMPROVEMENTS.md",
    "docs/ops/RUN_LOG.md",
    "docs/ops/IMPROVEMENTS_500.md",
    "docs/ops/IMPROVEMENTS_1000.md",
    "docs/ops/CODEX_CUSTOM_INSTRUCTIONS_PROMPT.md",
    "docs/ops/IP_INTEGRATION.md",
    "docs/ops/OBSERVABILITY.md",
    "docs/ops/SECURITY_HEADERS.md",
    "docs/ops/LOCALHOST_BINDING.md",
    "docs/ops/CHANGELOG_TEMPLATE.md",
    "docs/ops/ROLLBACK_PLAYBOOK.md",
    "docs/ops/MCP_GATEWAY_SECURITY.md",
    "docs/ops/HEALTH_CHECKS.md",
    "docs/ops/BRANCH_CONSOLIDATION.md",
    "docs/ops/HEADY_KINETIC_RUNBOOK.md",
    "docs/ops/HEADY_BIO_LIMITS.md",
    "docs/ops/ADMIN_UI.md",
    "docs/ops/FOUNDATION_UI.md",
    "docs/ops/HEADY_VERTICALS_PHASES.md",
    "docs/ops/LIVING_FEDERATION_RUNBOOK.md",
    "docs/ops/LIVING_FEDERATION_MANIFEST.md",
    "docs/ops/ITERATION_SCRIPTS_PROMPT.md",
    "docs/ops/ITERATION_SCRIPTS_RUNBOOK.md",
    "docs/ops/GENESIS_DASHBOARD_RUNBOOK.md",
    "docs/ops/UPTIME_KUMA.md",
    "docs/security/identity/SPIFFE_SPIRE.md",
    "docs/security/identity/SPIRE_ROTATION.md",
    "docs/sop/SOP_SPIRE_BOOTSTRAP.md",
    "docs/sop/SOP_HEADY_REFLECT.md",
    "docs/patents/README.md",
    "docs/patents/SCAFFOLDING.md",
    "docs/patents/ASSIGNMENTS.md",
    "docs/patents/INVENTION_DISCLOSURE_INDEX.md",
    "docs/patents/PROVISIONAL_LINKS.md",
    "docs/patents/FILING_QUEUE.md",
    "docs/patents/invention_disclosures/IDF-20260122-03-heady-gaia.md",
    "docs/patents/invention_disclosures/IDF-20260122-04-patent-40-template.md",
    "docs/patents/invention_disclosures/IDF-20260122-05-heady-foundations.md",
    "docs/patents/invention_disclosures/IDF-20260122-06-living-federation.md",
    "docs/patents/invention_disclosures/IDF-20260122-07-demo-integrity-ledger.md",
    "docs/patents/invention_disclosures/IDF-20260122-08-demo-snapshot-export.md",
    "docs/patents/invention_disclosures/IDF-20260122-09-manifest-integrity-gate.md",
    "docs/patents/invention_disclosures/IDF-20260122-10-iteration-pipeline-orchestrator.md",
    "docs/patents/invention_disclosures/IDF-20260122-11-heady-kaizen.md",
    "docs/patents/invention_disclosures/IDF-20260122-12-optimistic-raa-edge-ui.md",
    "docs/patents/invention_disclosures/IDF-20260401-13-trust-layer-proof-pipeline.md",
    "docs/patents/invention_disclosures/IDF-20260402-14-heady-lens-body-map.md",
    "docs/patents/invention_disclosures/IDF-20260404-15-governed-builder-guardrails.md",
    "docs/patents/invention_disclosures/IDF-20260404-16-heady-make-proof-structure.md",
    "docs/patents/invention_disclosures/IDF-20260404-17-heady-field-regenerative-oracle.md",
    "docs/patents/invention_disclosures/IDF-20260404-18-heady-legacy-sovereign-succession.md",
    "docs/patents/invention_disclosures/IDF-20260406-19-branch-consolidation-orchestrator.md",
    "docs/patents/invention_disclosures/IDF-20260406-20-headykinetic-kinetic-governance.md",
    "docs/patents/invention_disclosures/IDF-20260406-21-pops-oracle-integrity-gate.md",
    "docs/patents/invention_disclosures/IDF-20260406-22-federated-vertical-intent-ledger.md",
    "docs/patents/invention_disclosures/IDF-20260406-23-zero-shot-voice-clone-orchestrator.md",
    "docs/patents/provisional/HS-PA-039_HeadyGaia_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-040_Patent40_Template_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-041_HeadyFoundations_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-042_LivingFederation_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-043_DemoIntegrityLedger_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-044_DemoSnapshotExport_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-045_ManifestIntegrityGate_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-046_IterationPipelineOrchestrator_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-047_HeadyKaizen_2026-01-22.docx",
    "docs/patents/provisional/HS-PA-049_TrustLayerProofPipeline_2026-04-01.docx",
    "docs/patents/provisional/HS-PA-050_HeadyLensBodyMap_2026-04-02.docx",
    "docs/patents/provisional/HS-PA-051_GovernedBuilderGuardrails_2026-04-04.docx",
    "docs/patents/provisional/HS-PA-052_HeadyMakeProofOfStructure_2026-04-04.docx",
    "docs/patents/provisional/HS-PA-053_HeadyFieldRegenerativeOracle_2026-04-04.docx",
    "docs/patents/provisional/HS-PA-054_HeadyLegacySovereignSuccession_2026-04-04.docx",
    "docs/patents/provisional/HS-PA-055_BranchConsolidationOrchestrator_2026-04-06.docx",
    "docs/patents/provisional/HS-PA-056_HeadyKinetic_2026-04-06.docx",
    "docs/patents/provisional/HS-PA-057_PoPSOracleIntegrity_2026-04-06.docx",
    "docs/patents/provisional/HS-PA-058_FederatedVerticalIntentLedger_2026-04-06.docx",
    "docs/patents/provisional/HS-PA-059_ZeroShotVoiceCloneOrchestrator_2026-04-06.docx",
    "docs/legal/PRIVACY_POLICY.md",
    "docs/legal/TOKEN_TERMS.md",
    "docs/business/PRICE_LIST.md",
    "docs/business/ROADMAP.md",
    "docs/business/TEAM_BIOS.md",
    "docs/business/TRUST_NARRATIVE.md",
    "docs/hardware/HEADY_GUARD_SCHEMATIC.md",
]

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        print("Missing required docs:")
        for path in missing:
            print(f"- {path}")
        return 1

    # Basic internal link validation for docs/INDEX.md
    index_path = ROOT / "docs/INDEX.md"
    content = index_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.strip().startswith("- [") and "(" in line and ")" in line:
            link = line.split("(", 1)[1].split(")", 1)[0]
            if link.startswith("http") or link.startswith("#"):
                continue
            target = (ROOT / link).resolve()
            if not target.exists():
                print(f"Broken link in docs/INDEX.md: {link}")
                return 1

    mkdocs_path = ROOT / "mkdocs.yml"
    mkdocs_raw = mkdocs_path.read_text(encoding="utf-8")
    nav_paths = set()
    for line in mkdocs_raw.splitlines():
        if "docs/" in line and ".md" in line:
            parts = line.split("docs/", 1)
            tail = parts[1].split("#", 1)[0].strip()
            candidate = f"docs/{tail.split()[0]}".rstrip(":")
            if candidate.endswith(".md"):
                nav_paths.add(candidate)

    missing_nav = []
    for path in sorted(nav_paths):
        nav_target = (ROOT / path).resolve()
        if not nav_target.exists():
            missing_nav.append(path)

    if missing_nav:
        print("Broken links in mkdocs.yml:")
        for path in missing_nav:
            print(f"- {path}")
        return 1

    print("Docs validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
