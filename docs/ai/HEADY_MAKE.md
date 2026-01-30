# HeadyMake (Proof-of-Structure)

## Purpose
HeadyMake provides cryptographic proof that each printed layer of an additive manufacturing job matches the intended CAD geometry. The system scans each layer, hashes the scan, compares it to the CAD reference slice, and signs the result. A complete build yields a tamper-evident certificate covering every layer.

## Architecture
- **Layer scanner**: laser/camera/interferometry rig captures geometry after each pass.
- **Geometry comparer**: aligns scan mesh to CAD slice and computes deviation metrics.
- **Attestation signer**: hashes scan + CAD slice and signs layer proofs.
- **Proof ledger**: append-only log (local or blockchain-backed) stores signed layer records.

## Transparency + Security
- HeadyReflect is invoked on every mismatch decision.
- PromptOps receipts capture any logic updates to scan thresholds.

## Validation
- `python3 apps/heady_make/proof_of_structure.py --demo`

## Patent Alignment
- Patent 35 (Proof-of-Structure — assigned to HeadySystems Inc.).
