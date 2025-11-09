from typing import Dict, Any, List, Optional
import time, os
from flask import current_app
from . import storage

PLAN_ENV_MAP = {
    "starter": "STRIPE_PRICE_STARTER",
    "pro": "STRIPE_PRICE_PRO",
    "enterprise": "STRIPE_PRICE_ENTERPRISE",
}

def price_map_from_env() -> Dict[str, str]:
    """Return {plan_name: price_id} pulled from environment (Flask config)."""
    m = {}
    for plan, env_key in PLAN_ENV_MAP.items():
        val = current_app.config.get(env_key) or os.getenv(env_key)
        if val:
            m[plan] = val
    return m

def plan_from_price_id(price_id: Optional[str]) -> Optional[str]:
    if not price_id:
        return None
    pm = price_map_from_env()
    for plan, pid in pm.items():
        if pid == price_id:
            return plan
    return None

def apply_event(evt: Dict[str, Any]) -> Dict[str, Any]:
    """Apply a billing-related event to in-memory state and keep a ring buffer of last events."""
    et = (evt or {}).get("type", "")
    data = (evt or {}).get("data", {})
    obj = data.get("object", {}) if isinstance(data, dict) else {}
    # Append to event log
    storage.add_billing_event({
        "type": et,
        "ts": int(time.time()),
        "id": evt.get("id"),
        "summary": {
            "status": obj.get("status"),
            "price_id": (obj.get("items",{}) or {}).get("data",[{}])[0].get("price",{}).get("id") if "items" in obj else None
        }
    })

    state_update = {}
    if et.startswith("customer.subscription."):
        items = (obj.get("items", {}) or {}).get("data", [])
        price_id = (items[0].get("price") or {}).get("id") if items else None
        state_update = {
            "subscription_status": obj.get("status"),
            "price_id": price_id,
            "plan": plan_from_price_id(price_id),
            "current_period_end": obj.get("current_period_end"),
        }
    elif et == "checkout.session.completed":
        price_id = (obj.get("display_items", [{}])[0].get("plan") or {}).get("id") if obj.get("display_items") else obj.get("subscription")  # best-effort
        state_update = {
            "last_checkout_status": obj.get("status"),
            "price_id": price_id or state_update.get("price_id"),
            "plan": plan_from_price_id(price_id) if price_id else storage.get_billing_state().get("plan")
        }
    else:
        # No-op for other events
        pass

    if state_update:
        storage.set_billing_state(state_update)

    return storage.get_billing_state()

def prices_descriptor() -> Dict[str, Any]:
    pm = price_map_from_env()
    return {
        "currency": "usd",
        "interval": "month",
        "plans": {
            "starter": {"price_id": pm.get("starter"), "label": "Starter", "amount_usd": 99},
            "pro": {"price_id": pm.get("pro"), "label": "Pro", "amount_usd": 300},
            "enterprise": {"price_id": pm.get("enterprise"), "label": "Enterprise", "amount_usd": 900}
        }
    }
