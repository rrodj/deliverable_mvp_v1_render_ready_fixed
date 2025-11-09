from flask import Blueprint, jsonify, request
from ..services.auth import require_auth
from ..services import storage
import datetime

bp = Blueprint("reports", __name__)

@bp.get("/weekly")
@require_auth
def weekly():
    week = request.args.get("week")
    now = datetime.datetime.utcnow()
    if not week:
        iso_year, iso_week, _ = now.isocalendar()
        week = f"{iso_year}-W{iso_week:02d}"

    result = {
        "week": week,
        "totals": {
            "menu_items": len(storage.list_menu_items()),
            "calibrations": len(storage.list_calibrations()),
            "alerts": len(storage.list_alerts())
        },
        "notes": [
            "Counts are based on in-memory state in MVP scaffold."
        ]
    }
    return jsonify(result), 200

@bp.get("/roi")
@require_auth
def roi_summary():
    # Compose ROI from current alerts and conservative seed
    try:
        from ..services.roi import monthly_roi_summary
    except Exception as e:
        return jsonify({"error": "roi_module_missing", "detail": str(e)}), 500

    alerts = storage.list_alerts()
    summary = monthly_roi_summary(alerts=alerts)
    return jsonify(summary), 200
