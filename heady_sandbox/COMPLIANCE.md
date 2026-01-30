# HeadySandbox Compliance Notice

HeadySandbox is a clinical testing environment intended for HIPAA-sensitive workflows.

## Requirements

- **Encrypted tunnel required**: All traffic must traverse an encrypted tunnel (TLS or VPN).
- **No production PHI**: Use synthetic or de-identified data unless explicitly authorized.
- **PII scrubbing enabled**: Incoming payloads are masked before logging.
- **Mode switching**: Clinical mode must be explicitly enabled for clinical testing.

## Scope

This node is isolated from other verticals and may only exchange routing metadata
with the HeadyConductor hub.
