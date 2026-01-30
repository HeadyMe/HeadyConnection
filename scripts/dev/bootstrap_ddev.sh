#!/usr/bin/env bash
set -euo pipefail

echo "[dev] Bootstrapping DDEV..." >&2

ddev start

ddev drush en heady_trust -y

ddev drush heady-trust:seed

if [[ "${ENABLE_HEADYCOIN:-0}" == "1" ]]; then
  ddev drush en heady_coin -y
  ddev drush heady-coin:seed
fi
