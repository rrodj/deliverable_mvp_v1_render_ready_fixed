from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-not-secret"),
        APP_ENV=os.getenv("APP_ENV", "development"),
        APP_VERSION=os.getenv("APP_VERSION", "0.1.0-mvp"),
        CORS_ORIGINS=os.getenv("CORS_ORIGINS", "*"),
        DEMO_API_TOKEN=os.getenv("DEMO_API_TOKEN", "demo-token-please-change"),
        STRIPE_WEBHOOK_SECRET=os.getenv("STRIPE_WEBHOOK_SECRET"),
        STRIPE_PRICE_STARTER=os.getenv("STRIPE_PRICE_STARTER"),
        STRIPE_PRICE_PRO=os.getenv("STRIPE_PRICE_PRO"),
        STRIPE_PRICE_ENTERPRISE=os.getenv("STRIPE_PRICE_ENTERPRISE"),
        STRIPE_BILLING_PORTAL_URL=os.getenv("STRIPE_BILLING_PORTAL_URL")
    )
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"].split(",") if app.config["CORS_ORIGINS"] != "*" else "*"}})

    from .routes.health import bp as health_bp
    from .routes.auth import bp as auth_bp
    from .routes.uploads import bp as uploads_bp
    from .routes.calibrations import bp as calibrations_bp
    from .routes.alerts import bp as alerts_bp
    from .routes.reports import bp as reports_bp
    from .routes.webhooks import bp as webhooks_bp
    from .routes.billing import bp as billing_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(uploads_bp, url_prefix="/uploads")
    app.register_blueprint(calibrations_bp, url_prefix="/calibrations")
    app.register_blueprint(alerts_bp, url_prefix="/alerts")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(webhooks_bp, url_prefix="/webhooks")
    app.register_blueprint(billing_bp, url_prefix="/billing")

    @app.errorhandler(404)
    def _not_found(e):
        return jsonify({"error": "not_found"}), 404

    @app.errorhandler(500)
    def _server_error(e):
        return jsonify({"error": "server_error"}), 500

    return app

app = create_app()
