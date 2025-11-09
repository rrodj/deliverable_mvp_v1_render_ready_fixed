-- Inventory Guardian — Database Schema (PostgreSQL-first)
-- Generated: 2025-11-06T06:24:30Z
BEGIN;

CREATE TABLE IF NOT EXISTS organizations (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  password_hash TEXT,
  role TEXT NOT NULL DEFAULT 'admin',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS devices (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  device_type TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS calibrations (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  device_id TEXT NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
  offset NUMERIC(10,4) NOT NULL,
  note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by TEXT REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_calibrations_device_created ON calibrations(device_id, created_at DESC);

CREATE TABLE IF NOT EXISTS menu_uploads (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  uploaded_by TEXT REFERENCES users(id),
  source_filename TEXT,
  uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS menu_items (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  upload_id TEXT REFERENCES menu_uploads(id) ON DELETE SET NULL,
  sku TEXT NOT NULL,
  name TEXT NOT NULL,
  price NUMERIC(10,2),
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (org_id, sku)
);
CREATE INDEX IF NOT EXISTS idx_menu_items_org_created ON menu_items(org_id, created_at DESC);

CREATE TABLE IF NOT EXISTS alerts (
  id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  message TEXT NOT NULL,
  level TEXT NOT NULL CHECK (level IN ('info','warning','critical')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  acknowledged BOOLEAN NOT NULL DEFAULT false,
  acknowledged_at TIMESTAMPTZ,
  acknowledged_by TEXT REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_alerts_org_created ON alerts(org_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_unacked ON alerts(org_id) WHERE acknowledged = false;

CREATE TABLE IF NOT EXISTS webhook_events (
  id TEXT PRIMARY KEY,
  org_id TEXT REFERENCES organizations(id) ON DELETE SET NULL,
  provider TEXT NOT NULL,
  event_type TEXT,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  payload_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_webhook_provider_time ON webhook_events(provider, received_at DESC);

COMMIT;
