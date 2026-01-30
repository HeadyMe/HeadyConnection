#!/usr/bin/env bash
set -euo pipefail

LOCK_FILE="${1:-governance.lock.json}"

if [[ ! -f "$LOCK_FILE" ]]; then
  echo "Governance lock file not found: $LOCK_FILE" >&2
  exit 1
fi

echo "[governance] Stub installer - download policy pack from canonical governance repo." >&2
echo "[governance] Update governance.lock.json with the real release asset before use." >&2
