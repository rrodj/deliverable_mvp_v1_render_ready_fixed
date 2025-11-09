# Backend Spec — Inventory Guardian (MVP)

**Generated:** 2025-11-06T06:24:30Z

Endpoints:
- `GET /healthz` — liveness probe
- `POST /auth/login` — returns token stub
- `POST /uploads/menus` — multipart CSV upload
- `GET/POST /calibrations` — list/create
- `GET /alerts` — list alerts
- `POST /alerts/test` — inject a test alert
- `GET /reports/weekly` — aggregate report
- `POST /webhooks/stripe` — Stripe webhook receiver (verification stub)

Config: `.env.example`. No real secrets included.
