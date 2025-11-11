#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Prefer Render venv python if present, else fall back
PY_CANDIDATES=(
  "/opt/render/project/src/.venv/bin/python"
  "./.venv/bin/python"
  "python3"
  "python"
)
for p in "${PY_CANDIDATES[@]}"; do
  if command -v "$p" >/dev/null 2>&1; then
    PY="$p"
    break
  fi
done

if [ -z "${PY:-}" ]; then
  echo "No python interpreter found" >&2
  exit 127
fi

export PORT="${PORT:-8000}"
exec "$PY" -m gunicorn wsgi:app --workers 2 --threads 8 --bind 0.0.0.0:"$PORT"
