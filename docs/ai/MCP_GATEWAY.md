# MCP Gateway

The MCP gateway enforces host/origin allowlists, JWT validation, destructive tool confirmation, and optional HeadyReflect checks.

## Config Validation
The gateway validates upstream definitions on startup (unique names, valid URLs, and non-empty tool allowlists). Startup will fail fast if the config is invalid.

## Rate Limiting
Set `RATE_LIMIT_RPS` and `RATE_LIMIT_WINDOW_MS` to control per-client request limits. `RATE_LIMIT_TTL_MS` controls eviction of idle rate buckets.

## CORS + Request IDs
If the request origin is allowed, the gateway emits CORS headers and includes an `x-request-id` header on every response for traceability.

## Verification
- `curl http://127.0.0.1:8081/health`
- Verify `x-request-id` in responses and JSON logs for tracing.
