# Health Check Expectations

Core services should expose `/health` and respond with `status: ok`.

## Current Endpoints
- MCP Gateway: `http://127.0.0.1:8081/health`
- HeadyConductor: `http://127.0.0.1:8000/health`
- Verticals: `http://127.0.0.1:8000/health`

## Verification
Use `curl -s -D -` and confirm HTTP 200 plus an `x-request-id` header for traceability.
