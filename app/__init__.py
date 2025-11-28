import os
from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from sqlalchemy import text
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()

def create_app():

    # FORCE load .env from the backend root directory
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(backend_root, ".env")

    print("Loading .env from:", env_path)

    load_dotenv(env_path)

    # DEBUG: Check if env variables are loaded
    print("DATABASE_URL:", os.environ.get('DATABASE_URL'))
    print("JWT_SECRET_KEY:", os.environ.get('JWT_SECRET_KEY'))

    app = Flask(__name__)

     # Enable CORS for all routes (allowing all origins, you can restrict later)
    CORS(app, supports_credentials=True)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/smart_cane_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.vip import vip_bp
    from app.routes.guardian import guardian_bp
    from app.routes.location import location_bp
    from app.routes.reminders import reminders_bp
    from app.routes.alerts import alerts_bp
    from app.routes.qr import qr_bp
    from app.routes.device_guardian import device_guardian_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(vip_bp, url_prefix='/api/vip')
    app.register_blueprint(guardian_bp, url_prefix='/api/guardian')
    app.register_blueprint(location_bp, url_prefix='/api/location')
    app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(device_guardian_bp, url_prefix='/api/device-guardian')
    app.register_blueprint(qr_bp, url_prefix='/api/qr')

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request",
            "details": str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
    
    @app.route("/api/test-db")
    def test_db():
        try:
            # Wrap SQL query in text() for SQLAlchemy 2.x
            result = db.session.execute(text("SELECT 1")).fetchone()
            return {
                "success": True,
                "message": "Database connected!",
                "result": result[0]
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Database connection failed",
                "error": str(e)
            }

    return app
