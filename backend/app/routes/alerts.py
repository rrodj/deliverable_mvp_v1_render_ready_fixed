from flask import Blueprint, jsonify
from ..services.auth import require_auth
from ..services import storage

bp = Blueprint("alerts", __name__)

@bp.get("")
@require_auth
def list_all():
    return jsonify(storage.list_alerts()), 200

@bp.post("/test")
@require_auth
def create_test():
    a = storage.add_alert("test", "This is a test alert", "info")
    return jsonify(a), 201
