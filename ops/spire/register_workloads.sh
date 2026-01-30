#!/usr/bin/env bash
set -euo pipefail

SPIFFE_ID="${SPIFFE_ID:-spiffe://example.heady/ns/default/sa/web}"
SELECTORS="${SELECTORS:-k8s:ns:default,k8s:sa:web}"

echo "[spire] Example workload registration helper." >&2
if [[ "$SPIFFE_ID" == *"example.heady"* ]]; then
  echo "[spire] NOTE: update SPIFFE_ID to your real trust domain before production use." >&2
fi

selector_args=()
IFS=',' read -r -a selector_items <<< "$SELECTORS"
for selector in "${selector_items[@]}"; do
  selector_args+=("-selector" "$selector")
done

echo "spire-server entry create -spiffeID ${SPIFFE_ID} ${selector_args[*]}" >&2
