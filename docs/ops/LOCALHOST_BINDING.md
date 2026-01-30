# Localhost Binding Policy

All internal services must bind to `127.0.0.1` unless explicitly documented.

## Rationale
- Reduces attack surface.
- Enforces tunnel-only origin posture.

## Verification
Use `ss -lntp` or `lsof -iTCP -sTCP:LISTEN` to verify bindings.

## Compose Defaults
The root `docker-compose.yml` maps the conductor port to `127.0.0.1` to align with this policy.
