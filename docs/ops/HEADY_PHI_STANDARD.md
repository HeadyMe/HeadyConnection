# Heady Phi Standard

Heady Phi (ϕ) is the default scaling constant used for retries, growth, and decay.

## Principles
- Deterministic math with explicit rounding.
- Jitter is bounded by a Phi window.
- Prefer additive integration over replacing existing safety guards.

## Reference Implementation
See `ops/tools/lib_heady_phi.py` for a minimal Python helper.
