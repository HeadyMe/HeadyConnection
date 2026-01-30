# Cloudflare Tunnel

This repo is designed for tunnel-only origin posture. Bind origin services to localhost and use Cloudflare Tunnel for ingress.

## Notes
- Do not enable `noTLSVerify` unless explicitly documented and approved.
- Store tunnel credentials outside the repo.
- Use least-privilege tokens.

## Template
Create a `config.yml` outside the repo based on this structure:

```yaml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/<tunnel-id>.json

ingress:
  - hostname: trust.example.com
    service: http://127.0.0.1:8080
  - service: http_status:404
```

## Edge UI Template
See `ops/cloudflare/edge-ui/` for a worker-based status UI scaffold.
