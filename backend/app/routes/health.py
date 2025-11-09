from flask import Blueprint, jsonify, current_app

bp = Blueprint("health", __name__)

@bp.get("/healthz")
def healthz():
    return jsonify({
        "status": "ok",
        "version": current_app.config.get("APP_VERSION", "unknown"),
        "env": current_app.config.get("APP_ENV", "development")
    }), 200
