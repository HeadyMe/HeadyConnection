#!/usr/bin/env bash
set -euo pipefail

HOOKS_DIR=".githooks"

git config core.hooksPath "$HOOKS_DIR"
echo "[governance] Git hooks path set to $HOOKS_DIR" >&2
