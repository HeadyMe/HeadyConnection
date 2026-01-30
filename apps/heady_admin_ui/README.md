# Heady Admin UI

Unified personal admin dashboard and control panel for tasks, documents, calendar, communications, and finance.

## Structure
- `backend/`: Express API with audit logging and token-based auth.
- `frontend/`: React + Vite UI.
- `docs/`: Architecture notes and API usage.

## Run (Local)
```bash
cd apps/heady_admin_ui/backend
cp .env.example .env
npm install
npm run start
```

```bash
cd apps/heady_admin_ui/frontend
npm install
npm run dev
```

## API Auth
Send `Authorization: Bearer <HEADY_ADMIN_TOKEN>` with each request.

## Validation
```bash
node apps/heady_admin_ui/scripts/validate_api_contract.js
node apps/heady_admin_ui/scripts/lint_placeholders.js
python3 scripts/web/validate_heady_admin_ui.py
```
