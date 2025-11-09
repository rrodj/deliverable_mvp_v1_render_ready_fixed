from flask import Blueprint, request, jsonify, current_app
import json

bp = Blueprint("webhooks", __name__)

@bp.post("/stripe")
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig = request.headers.get("Stripe-Signature")
    secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")
    try:
        data = json.loads(payload) if payload else {}
    except Exception:
        return jsonify({"error": "invalid_json"}), 400

    # Basic acceptance: event parsed. "verified" is true only if header+secret present (MVP stub).
    verified = bool(secret and sig)

    # Apply to billing state (no-op if unrelated type)
    try:
        from ..services import billing as billing_svc
        state = billing_svc.apply_event(data)
    except Exception as e:
        state = {"error": "billing_apply_failed", "detail": str(e)}

    return jsonify({"received": True, "verified": verified, "event_type": data.get("type"), "billing_state": state}), 200
