# Heady Admin UI Architecture

## Overview
The admin UI is split into a frontend (React + Vite) and backend (Express). The backend exposes CRUD endpoints for core modules and records every mutation in an audit log.

## Modules
- User Profile & Authentication
- Tasks & Projects
- Documents & Content
- Calendar & Scheduling
- Communications
- Finance & Subscriptions
- Analytics & Reporting (planned)
- Settings & Customization

## Security
- Token-based auth (`HEADY_ADMIN_TOKEN`).
- Helmet + CORS.
- Audit log stored in memory (swap to persistent storage before production).

## Audit & Versioning
Each create/update/delete operation emits an audit record. Soft-delete and versioning are modeled in `schema.sql` for production implementation.
