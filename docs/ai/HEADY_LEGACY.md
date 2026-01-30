# HeadyLegacy (Sovereign Succession)

## Purpose
HeadyLegacy orchestrates secure succession of self-sovereign keys. A biometric monitor detects inactivity, triggers a validated waiting period, and reconstructs the key from distributed shards using multi-party controls.

## Architecture
- **Biometric signal**: wearable heartbeat sensor produces signed liveness attestations.
- **Succession gate**: dead-man’s switch checks inactivity plus manual overrides.
- **Shard recovery**: Shamir secret sharing with quorum approval.
- **Transfer contract**: moves assets to designated heirs after verification.

## Transparency + Security
- HeadyReflect audits every succession decision.
- PromptOps receipts capture policy changes to inactivity thresholds.

## Validation
- `python3 apps/heady_legacy/sovereign_succession.py --demo`

## Patent Alignment
- Patent 37 (Sovereign Succession — assigned to HeadySystems Inc.).
