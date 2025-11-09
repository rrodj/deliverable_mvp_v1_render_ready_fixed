# Inventory Guardian — MVP Bundle

**Build:** 2025-11-06T06:24:30Z

This archive contains the complete MVP scaffold:
- `backend/` — Flask API
- `frontend/` — React (Vite) app (Vite root in `frontend/`; `package.json` and `vite.config.ts` at repo root)
- `db/` — SQL schema + ORM + migrations plan + seed
- `integrations/` — Stripe/Metrc/scheduler stubs (read-only)
- `deploy/` — Dockerfiles, Compose, Nginx, CI, Terraform stubs

## Quick Start (Docker Compose)
From the `deploy/` directory:
```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
# Frontend: http://localhost:8080
# Backend:  http://localhost:8000/healthz
```
The compose file builds using context `..` to include `backend/` and `frontend/`.

## Local Dev (separate terminals)
**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
npm ci || npm install
npm run dev   # http://localhost:5173
```

## Auth (MVP)
Use header `Authorization: Bearer demo-token-please-change` (or change via env).

## Structure Overview
```
backend/        Flask app + OpenAPI
frontend/       Vite app (React + TS)
db/             schema.sql, orm_models.py, migration_plan.md, seed_example.sql
integrations/   stripe.md, metrc.md, scheduler.md, stubs, examples, config/.env.example
deploy/         Dockerfiles, docker-compose.yml, nginx.conf, ci/, terraform/
package.json    root for Vite build scripts
vite.config.ts  Vite config (root points to ./frontend)
```
