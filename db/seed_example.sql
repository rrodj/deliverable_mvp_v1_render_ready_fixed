-- Seed Example (safe demo data)
BEGIN;

INSERT INTO organizations (id, name) VALUES ('org_demo_coastal', 'Demo Coastal') ON CONFLICT (id) DO NOTHING;
INSERT INTO users (id, org_id, email, name, role) VALUES ('user_admin_demo', 'org_demo_coastal', 'admin@example.com', 'Demo Admin', 'admin') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, org_id, name, device_type) VALUES ('scale-1', 'org_demo_coastal', 'Front Counter Scale', 'scale') ON CONFLICT (id) DO NOTHING;
INSERT INTO calibrations (id, org_id, device_id, offset, note, created_by) VALUES ('cal-1', 'org_demo_coastal', 'scale-1', -0.3000, 'initial calibration', 'user_admin_demo') ON CONFLICT (id) DO NOTHING;
INSERT INTO menu_uploads (id, org_id, uploaded_by, source_filename) VALUES ('upl-1', 'org_demo_coastal', 'user_admin_demo', 'menu.csv') ON CONFLICT (id) DO NOTHING;
INSERT INTO menu_items (id, org_id, upload_id, sku, name, price) VALUES
  ('item-1', 'org_demo_coastal', 'upl-1', 'A1', 'Widget', 9.99),
  ('item-2', 'org_demo_coastal', 'upl-1', 'B2', 'Gadget', 14.50)
ON CONFLICT (id) DO NOTHING;
INSERT INTO alerts (id, org_id, type, message, level) VALUES ('alert-1', 'org_demo_coastal', 'test', 'This is a test alert', 'info') ON CONFLICT (id) DO NOTHING;
INSERT INTO webhook_events (id, org_id, provider, event_type, payload_json) VALUES ('evt-1', 'org_demo_coastal', 'stripe', 'checkout.session.completed', '{"type":"checkout.session.completed"}') ON CONFLICT (id) DO NOTHING;

COMMIT;
