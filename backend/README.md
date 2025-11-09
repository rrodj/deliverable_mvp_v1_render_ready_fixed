# Inventory Guardian — Backend Scaffold

**Generated:** 2025-11-06T06:24:30Z

Minimal Flask scaffold for the MVP:
- Auth (token stub), Menus upload (CSV), Calibrations, Alerts, Weekly Reports
- Stripe webhook endpoint (verification stub)
- Health check
- OpenAPI spec

## Quickstart (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
flask --app app run --host 0.0.0.0 --port 8000
# http://localhost:8000/healthz
```

## Auth stub
Send `Authorization: Bearer $DEMO_API_TOKEN` where `$DEMO_API_TOKEN` is from `.env.example` (default: `demo-token-please-change`).
