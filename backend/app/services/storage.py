import uuid, datetime

STATE = {
    "menus": [],
    "calibrations": [],
    "alerts": [],
    "billing": {},
    "billing_events": []
}

def add_menu_items(items):
    STATE["menus"].extend(items)

def list_menu_items():
    return STATE["menus"]

def add_calibration(device_id, offset, note=None):
    c = {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "offset": float(offset),
        "note": note,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    STATE["calibrations"].append(c)
    return c

def list_calibrations():
    return STATE["calibrations"]

def add_alert(alert_type, message, level="info"):
    a = {
        "id": str(uuid.uuid4()),
        "type": alert_type,
        "message": message,
        "level": level,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    STATE["alerts"].append(a)
    return a

def list_alerts():
    return STATE["alerts"]

# --- Billing helpers (new) ---
def add_billing_event(evt):
    buf = STATE.setdefault("billing_events", [])
    buf.append(evt)
    # keep last 50
    if len(buf) > 50:
        del buf[:-50]

def list_billing_events():
    return list(STATE.get("billing_events", []))

def get_billing_state():
    return dict(STATE.get("billing", {}))

def set_billing_state(update):
    cur = STATE.setdefault("billing", {})
    cur.update({k: v for k, v in (update or {}).items() if v is not None})
    return cur
