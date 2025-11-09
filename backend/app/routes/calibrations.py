from flask import Blueprint, request, jsonify
from ..services.auth import require_auth
from ..services import storage

bp = Blueprint("calibrations", __name__)

@bp.get("")
@require_auth
def list_all():
    return jsonify(storage.list_calibrations()), 200

@bp.post("")
@require_auth
def create():
    data = request.get_json(silent=True) or {}
    device_id = data.get("device_id")
    offset = data.get("offset")
    note = data.get("note")
    if device_id is None or offset is None:
        return jsonify({"error": "missing_fields", "required": ["device_id", "offset"]}), 400
    try:
        cal = storage.add_calibration(device_id, offset, note)
    except Exception as e:
        return jsonify({"error": "invalid_payload", "detail": str(e)}), 400
    return jsonify(cal), 201
