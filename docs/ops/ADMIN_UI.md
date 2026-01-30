# Personal Admin UI (Heady Admin)

## Purpose
The Heady Admin UI provides a unified dashboard and control panel for managing tasks, documents, calendars, communications, finance, and settings.

## Location
- `apps/heady_admin_ui/`

## Run
```bash
cd apps/heady_admin_ui
docker compose up
```

## Validation
```bash
make admin-ui-validate
```

## Security Notes
- Token-based auth (`HEADY_ADMIN_TOKEN`).
- Audit log records every mutation.
- Soft-delete + versioning modeled in `schema.sql` for production implementation.
