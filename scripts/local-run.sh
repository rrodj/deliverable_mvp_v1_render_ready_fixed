#!/usr/bin/env bash
# Local dev runner for the backend. Picks a free port automatically.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# 1) Python venv
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

# 2) Install deps
python -m pip install --upgrade pip >/dev/null
python -m pip install -r backend/requirements.txt

# 3) Choose a free port (start at 8000 and increment)
if [ -z "${PORT:-}" ]; then
  PORT=8000
fi
probe="$PORT"
while lsof -iTCP:"$probe" -sTCP:LISTEN -n >/dev/null 2>&1; do
  probe=$((probe+1))
done
export PORT="$probe"

export APP_ENV=development
export DEMO_API_TOKEN="${DEMO_API_TOKEN:-demo-token-please-change}"

echo "▶ Starting backend on http://127.0.0.1:$PORT (0.0.0.0:$PORT)"
echo "   Healthcheck: curl -sSf http://127.0.0.1:$PORT/healthz && echo OK"
cd backend
exec python -m gunicorn wsgi:app --bind 0.0.0.0:"$PORT"
