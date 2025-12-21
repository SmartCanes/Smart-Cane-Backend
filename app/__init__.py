import os
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from flask_cors import CORS

from app.utils.responses import error_response


db = SQLAlchemy()
jwt = JWTManager()

limiter = Limiter(
    key_func=get_remote_address, default_limits=[], storage_uri="memory://"
)


def register_limiter_handlers(app: Flask):
    @app.errorhandler(429)
    def rate_limit_handler(e):
        return error_response(
            "Too many requests. Please try again later.",
            status_code=429,
            details=str(e),  # optional, you can remove if you don't need it
        )


def create_app():
    DEV_MODE = os.environ.get("DEV_MODE", "development") == "development"
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(backend_root, ".env")

    print("Loading .env from:", env_path)

    load_dotenv(env_path)

    # DEBUG: Check if env variables are loaded
    print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
    print("JWT_SECRET_KEY:", os.environ.get("JWT_SECRET_KEY"))
    print("FRONTEND_URL:", os.environ.get("FRONTEND_URL"))

    app = Flask(__name__)

    if DEV_MODE:
        app.config["JWT_COOKIE_SECURE"] = False
        app.config["JWT_COOKIE_SAMESITE"] = "Lax"
        CORS(
            app,
            supports_credentials=True,
            resources={
                r"/*": {
                    "origins": os.environ.get("FRONTEND_URL", "http://localhost:5173")
                }
            },
        )
    else:
        app.config["JWT_COOKIE_SECURE"] = True
        app.config["JWT_COOKIE_SAMESITE"] = "None"
        CORS(
            app,
            supports_credentials=True,
            resources={r"/*": {"origins": "https://yourdomain.com"}},
        )

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3306/smart_cane_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "secret-key")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    # Local dev only
    # app.config['JWT_COOKIE_SECURE'] = True
    # app.config['JWT_COOKIE_SAMESITE'] = 'None'

    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    register_limiter_handlers(app)

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            # Respond with 200 OK and CORS headers
            response = jsonify({"success": True})
            response.status_code = 200
            return response

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.vip import vip_bp
    from app.routes.guardian import guardian_bp
    from app.routes.location import location_bp
    from app.routes.reminders import reminders_bp
    from app.routes.alerts import alerts_bp
    from app.routes.device_pairing import device_pairing_bp
    from app.routes.device_guardian import device_guardian_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vip_bp, url_prefix="/api/vip")
    app.register_blueprint(guardian_bp, url_prefix="/api/guardian")
    app.register_blueprint(location_bp, url_prefix="/api/location")
    app.register_blueprint(reminders_bp, url_prefix="/api/reminders")
    app.register_blueprint(alerts_bp, url_prefix="/api/alerts")
    app.register_blueprint(device_guardian_bp, url_prefix="/api/device-guardian")
    app.register_blueprint(device_pairing_bp, url_prefix="/api/device")

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "Bad request",
                    "details": str(error),
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    @app.route("/api/test-db")
    def test_db():
        try:
            # Wrap SQL query in text() for SQLAlchemy 2.x
            result = db.session.execute(text("SELECT 1")).fetchone()
            return {
                "success": True,
                "message": "Database connected!",
                "result": result[0],
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Database connection failed",
                "error": str(e),
            }

    return app
