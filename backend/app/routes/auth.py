from flask import Blueprint, jsonify, request, current_app

bp = Blueprint("auth", __name__)

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "invalid_credentials"}), 400
    token = current_app.config.get("DEMO_API_TOKEN", "demo-token-please-change")
    return jsonify({"access_token": token, "token_type": "Bearer"}), 200
