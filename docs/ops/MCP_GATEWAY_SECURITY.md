# MCP Gateway Security Controls

## Controls
- Host allowlist
- Origin allowlist (optional strict requirement)
- JWT/JWKS validation with optional audience check
- Rate limiting per client
- Payload size limits
- Destructive tool confirmation
- Request ID header for traceability
- Config validation on startup (fail fast if invalid)

## Configuration
- `RATE_LIMIT_RPS`
- `RATE_LIMIT_WINDOW_MS`
- `RATE_LIMIT_TTL_MS`
- `MAX_BODY_BYTES`
- `STRICT_ORIGIN`
- `JWT_AUDIENCE`

## Verification
Run `curl http://127.0.0.1:8081/health` and check JSON logs for rate-limit events.
