#!/usr/bin/env bash
set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
TOKEN="${TOKEN:-}"

function get_token() {
  if [[ -n "${TOKEN}" ]]; then
    echo "${TOKEN}"
    return
  fi
  echo "→ Logging in (stub)"
  token=$(curl -sS -X POST "${BACKEND_URL}/auth/login" -H "Content-Type: application/json" --data '{"username":"demo","password":"demo"}' | jq -r '.access_token' 2>/dev/null || true)
  if [[ -z "${token}" || "${token}" == "null" ]]; then
    token="demo-token-please-change"
  fi
  echo "${token}"
}

authz() {
  echo "Authorization: Bearer $1"
}

TOKEN="$(get_token)"

echo "→ Alerts: create test alert"
curl -sS -X POST "${BACKEND_URL}/alerts/test" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "→ Reports: weekly"
curl -sS "${BACKEND_URL}/reports/weekly" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "→ Reports: ROI"
curl -sS "${BACKEND_URL}/reports/roi" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "→ Billing: prices"
curl -sS "${BACKEND_URL}/billing/prices" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "→ Billing: status (before events)"
curl -sS "${BACKEND_URL}/billing/status" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "→ Webhook: send sample checkout.session.completed"
curl -sS "${BACKEND_URL}/webhooks/stripe" -H "Content-Type: application/json" -H "Stripe-Signature: t=0,v1=stub" --data @samples/stripe/checkout.session.completed.json | (jq . 2>/dev/null || cat)

echo "→ Webhook: send sample customer.subscription.created"
curl -sS "${BACKEND_URL}/webhooks/stripe" -H "Content-Type: application/json" -H "Stripe-Signature: t=0,v1=stub" --data @samples/stripe/customer.subscription.created.json | (jq . 2>/dev/null || cat)

echo "→ Billing: status (after events)"
curl -sS "${BACKEND_URL}/billing/status" -H "$(authz "${TOKEN}")" | (jq . 2>/dev/null || cat)

echo "✓ Smoke complete"
