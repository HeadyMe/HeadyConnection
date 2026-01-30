# Security Headers Baseline

Recommended headers for the tunnel-only origin Nginx configuration.

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

Validate headers using `curl -I` against localhost before exposing via tunnel.
