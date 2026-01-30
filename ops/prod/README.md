# Production Topology

Production deployments assume a **tunnel-only origin**:

- Nginx and PHP-FPM bind to localhost.
- Cloudflare Tunnel is the only ingress.
- No direct public exposure of origin services.

## Components
- Nginx reverse proxy (localhost-only)
- PHP-FPM pool for Drupal
- Cloudflare Tunnel (`cloudflared`) running as a systemd service

## Templates
- `ops/prod/nginx.conf.example`
- `ops/prod/php-fpm.conf.example`

See `ops/cloudflare` for tunnel templates and `ops/systemd` for service scaffolding.
