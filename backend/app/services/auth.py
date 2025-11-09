from functools import wraps
from flask import current_app, request, jsonify

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1].strip()
        if not token:
            token = request.headers.get("X-API-Key")

        expected = current_app.config.get("DEMO_API_TOKEN")
        if not expected or token != expected:
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper
