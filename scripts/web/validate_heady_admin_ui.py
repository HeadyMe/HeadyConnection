#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "apps" / "heady_admin_ui"

REQUIRED = [
    "README.md",
    "docker-compose.yml",
    "backend/server.js",
    "backend/openapi.yaml",
    "backend/schema.sql",
    "backend/.env.example",
    "backend/package.json",
    "frontend/package.json",
    "frontend/index.html",
    "frontend/src/App.jsx",
    "frontend/src/main.jsx",
    "frontend/src/styles.css",
    "docs/ARCHITECTURE.md",
]

REQUIRED_PATHS = {
    "/api/profile",
    "/api/tasks",
    "/api/tasks/{id}",
    "/api/documents",
    "/api/documents/{id}",
    "/api/events",
    "/api/events/{id}",
    "/api/messages",
    "/api/messages/{id}",
    "/api/finance",
    "/api/finance/{id}",
    "/api/audit",
}


def main() -> int:
    missing = [path for path in REQUIRED if not (BASE / path).exists()]
    if missing:
        print("Missing admin UI files:")
        for path in missing:
            print(f"- {path}")
        return 1

    openapi_path = BASE / "backend" / "openapi.yaml"
    openapi_lines = openapi_path.read_text(encoding="utf-8").splitlines()
    paths_section = False
    discovered_paths = set()
    for line in openapi_lines:
        stripped = line.strip()
        if stripped == "paths:":
            paths_section = True
            continue
        if paths_section:
            if stripped and not line.startswith("  "):
                break
            if stripped.startswith("/") and stripped.endswith(":"):
                discovered_paths.add(stripped[:-1])

    missing_paths = REQUIRED_PATHS - discovered_paths
    if missing_paths:
        print("Missing required OpenAPI paths:")
        for path in sorted(missing_paths):
            print(f"- {path}")
        return 1

    print("Heady Admin UI validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
