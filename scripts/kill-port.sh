#!/usr/bin/env bash
set -euo pipefail
port="${1:-8000}"
pids=$(lsof -t -iTCP:"$port" -sTCP:LISTEN -n || true)
if [ -z "$pids" ]; then
  echo "No process is listening on port $port"
  exit 0
fi
echo "Killing PIDs: $pids on port $port"
kill -9 $pids
