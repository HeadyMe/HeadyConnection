# Heady MCP Gateway Sidecar

A localhost-bound MCP gateway that enforces allowlists, JWT validation, and optional HeadyReflect checks before routing tool calls to upstream servers.

## Features
- Localhost bind by default (`BIND_HOST=127.0.0.1`).
- Host and Origin allowlists.
- JWT validation via HS256 secret or JWKS URL.
- Tool allowlists per upstream server.
- Confirmation gate for destructive tools.
- Structured JSON logs.

## Environment
See `.env.example` for the full list of environment variables.

## Configuration
Copy `mcp.config.json.example` to `mcp.config.json` and update upstreams and tool allowlists.

## Development
```bash
npm install
npm run typecheck
npm run build
npm run start
```

## HeadyReflect Gate
Set `HEADY_REFLECT_ENFORCE=1` to require a minimal `reflection` object in tool requests.

## Optimistic RAA Flag
Set `OPTIMISTIC_RAA=1` to enable optimistic RAA logging (no behavior changes yet).
