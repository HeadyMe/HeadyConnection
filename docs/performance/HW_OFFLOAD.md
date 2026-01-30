# Hardware Offload

Hardware offload accelerates cryptographic verification and policy checks using specialized hardware (FPGA, DPU, or HSM). It is most effective when software profiling shows signature verification as the bottleneck.

## Candidate Workloads
- JWT verification at high throughput.
- PQC signature validation for receipts.
- TLS termination with hardware acceleration.

## Decision Criteria
- CPU utilization consistently above threshold.
- Verification latency exceeds SLOs.
- Cost of hardware is justified by workload volume.

## Governance Notes
- Ensure keys remain in secure hardware modules.
- Maintain deterministic logs and evidence receipts.
- Keep a software fallback path for outages.
