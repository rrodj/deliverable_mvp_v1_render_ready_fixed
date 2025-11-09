#!/usr/bin/env bash
set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

echo "→ Checking health at ${BACKEND_URL}/healthz"
code=$(curl -s -o /tmp/ig_health.json -w "%{http_code}" "${BACKEND_URL}/healthz" || true)
if [[ "$code" != "200" ]]; then
  echo "Health check failed (HTTP ${code})"
  cat /tmp/ig_health.json || true
  exit 1
fi
echo "OK"
cat /tmp/ig_health.json | (jq . 2>/dev/null || cat) || true
