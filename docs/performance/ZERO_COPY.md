# Zero-Copy Pathways

Zero-copy pathways reduce latency and CPU overhead by avoiding repeated memory copies between disk, application memory, and the network interface. This is most impactful for high-volume media, telemetry, or evidence payloads that are large but non-sensitive once governed.

## Goals
- Reduce CPU pressure during large transfers.
- Maintain governance boundaries by keeping control-plane checks separate from the data plane.
- Enable predictable throughput during peak loads.

## Recommended Patterns
1. **Object-store streaming:** Stream assets directly from storage to the client with `sendfile`-style APIs.
2. **Chunked content addressing:** Split large payloads into signed chunks and stream sequentially.
3. **Edge cache with provenance:** Cache only after receipt verification and allowlist checks.

## Governance Notes
- Never bypass RAA or policy checks for privileged payloads.
- Record content hashes and receipts before serving from cache.
- Keep zero-copy limited to assets classified as low-risk or public.

## Implementation Hooks
- Nginx `sendfile` for static assets behind the tunnel-only origin.
- Worker-based pass-through for edge UI assets.
- Evidence receipt pipeline for any cacheable blob.
