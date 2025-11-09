# LOCAL RUN — Inventory Guardian (MVP + Phase 4 patches)

**Generated:** 2025-11-06T21:54:21Z

This pack provides a **docker‑compose override** and **smoke test scripts** to validate the app locally.

## Prereqs
- Docker / Docker Compose
- `curl` (and optionally `jq` for pretty JSON)
- `.env` templates from `env_pack.zip` (placeholders only; fill locally)

## Start services
From repo root (sibling of `deploy/`, `backend/`, `frontend/`):
```bash
docker compose -f deploy/docker-compose.yml -f local/compose.override.yml up -d --build
# Frontend: http://localhost:8080
# Backend:  http://localhost:8000/healthz
```

> The override mounts env files and sets ports. For fast iteration, you can rebuild only the backend or frontend service with `docker compose build <service>`.

## Smoke tests
Run in order:

```bash
# 1) Health
bash scripts/healthz.sh

# 2) Core routes + ROI + Billing stubs
bash scripts/routes_smoke.sh
```

Expected highlights:
- `/healthz` → 200 JSON with `status: ok`
- Login returns a token; protected routes succeed
- `/reports/roi` returns `total_protected_usd`
- Stripe webhook accepts sample events and `/billing/status` shows recent events

## Environment
Create local env files (examples are in `env_pack.zip`):
```bash
cp .env.backend.example .env.backend
cp .env.frontend.example .env.frontend
cp .env.scheduler.example .env.scheduler
cp .env.metrc.example .env.metrc
cp .env.stripe.example .env.stripe
# Edit the new files locally — do NOT commit real secrets
```
Set at minimum for billing tests:
- `STRIPE_WEBHOOK_SECRET=whsec_test_placeholder` (any non-empty string enables "verified" flag for local tests)

## Tear down
```bash
docker compose -f deploy/docker-compose.yml -f local/compose.override.yml down
```
