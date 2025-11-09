from flask import Blueprint, jsonify, current_app
from ..services.auth import require_auth
from ..services import storage
from ..services import billing as billing_svc

bp = Blueprint("billing", __name__)

@bp.get("/prices")
@require_auth
def prices():
    return jsonify(billing_svc.prices_descriptor()), 200

@bp.get("/status")
@require_auth
def status():
    return jsonify({
        "state": storage.get_billing_state(),
        "events": storage.list_billing_events()
    }), 200

@bp.get("/portal")
@require_auth
def portal():
    url = current_app.config.get("STRIPE_BILLING_PORTAL_URL") or "https://billing-portal.example/placeholder"
    return jsonify({"portal_url": url}), 200
