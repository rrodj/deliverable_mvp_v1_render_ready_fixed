from flask import Blueprint, request, jsonify
from ..services.auth import require_auth
from ..services import storage
import csv, io

bp = Blueprint("uploads", __name__)

@bp.post("/menus")
@require_auth
def upload_menus():
    if "file" not in request.files:
        return jsonify({"error": "file_missing"}), 400
    f = request.files["file"]
    try:
        raw = f.read()
        try:
            s = raw.decode("utf-8")
        except UnicodeDecodeError:
            s = raw.decode("latin-1")
        reader = csv.DictReader(io.StringIO(s))
        items = []
        for row in reader:
            if not row:
                continue
            sku = (row.get("sku") or "").strip()
            name = (row.get("name") or "").strip()
            price = row.get("price")
            if not sku or not name:
                continue
            try:
                price = float(price) if price is not None and price != "" else None
            except ValueError:
                price = None
            items.append({"sku": sku, "name": name, "price": price})
        storage.add_menu_items(items)
        return jsonify({"items_ingested": len(items)}), 201
    except Exception as e:
        return jsonify({"error": "parse_error", "detail": str(e)}), 400
