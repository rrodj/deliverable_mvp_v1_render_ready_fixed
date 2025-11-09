# Test Plan — Backend Scaffold

## Smoke
- `GET /healthz` → 200 JSON

## Auth-required endpoints
Use header `Authorization: Bearer demo-token-please-change`

### Calibrations
- `GET /calibrations` → 200 list
- `POST /calibrations` JSON:
  {"device_id":"scale-1","offset":-0.3,"note":"initial calibration"}
  → 201

### Menus upload (CSV)
- `POST /uploads/menus` multipart `file`
  sku,name,price
  A1,Widget,9.99
  → 201 with `items_ingested`

### Alerts
- `GET /alerts` → 200
- `POST /alerts/test` → 201

### Weekly Report
- `GET /reports/weekly?week=2025-W45` → 200

### Stripe Webhook
- `POST /webhooks/stripe` with JSON `{ "type":"checkout.session.completed" }` → 200
