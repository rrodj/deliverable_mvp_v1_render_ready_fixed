# Deploy to Render – Inventory Guardian

## Build & Start Commands
- Backend build: `pip install -r requirements.txt`
- Backend start: `gunicorn wsgi:app --workers 2 --threads 8 --bind 0.0.0.0:$PORT`
- Frontend build: `npm ci && npm run build` (publish `frontend/dist`)

## Environment Variables
Add the keys from `config/env.example` to the backend service. `SECRET_KEY` must be strong.

## Blueprint flow (recommended)
1) New → Blueprint → pick this repo (branch main)
2) Confirm two resources appear (backend web + frontend static)
3) Backend → Environment → add vars from `config/env.example`
4) Apply → Deploy. Verify `https://<backend>/healthz` returns 200.

## Manual flow (fallback)
**Backend (Web Service)**
- Root Directory: `backend`
- Environment: Python 3
- Build: `pip install -r requirements.txt`
- Start: `gunicorn wsgi:app --workers 2 --threads 8 --bind 0.0.0.0:$PORT`
- Health Check: `/healthz`

**Frontend (Static)**
- Root: `.`
- Build: `npm ci && npm run build`
- Publish: `frontend/dist`
- Env: `VITE_API_BASE_URL` = backend URL (if not using blueprint)

## Database
None; in-memory storage. Migrations N/A.

## Local quick test
```bash
# From repo root
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r backend/requirements.txt

export PORT=8000 APP_ENV=development DEMO_API_TOKEN=demo-token-please-change
# Run from backend dir using the provided wsgi entrypoint
cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT
# In another shell:
curl -i http://localhost:8000/healthz
```
