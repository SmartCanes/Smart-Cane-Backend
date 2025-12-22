import os
from flask import Flask, app, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from sqlalchemy import text
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    DEV_MODE = os.environ.get("DEV_MODE", "development") == "development"
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(backend_root, ".env")

    print("Loading .env from:", env_path)

    load_dotenv(env_path)

    print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
    print("JWT_SECRET_KEY:", os.environ.get("JWT_SECRET_KEY"))
    print("FRONTEND_URL:", os.environ.get("FRONTEND_URL"))

    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    uploads_path = os.path.join(base_dir, 'uploads')

    app.config['UPLOAD_FOLDER'] = uploads_path
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
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

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3306/smart_cane_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "secret-key")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    db.init_app(app)
    jwt.init_app(app)

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            response = jsonify({"success": True})
            response.status_code = 200
            return response

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

    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        try:
            
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        except FileNotFoundError:

            return jsonify({"success": False, "error": "File not found"}), 404
        except Exception as e:
            print(f"Error serving file: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/debug-uploads')
    def debug_uploads():
        """Debug endpoint to check upload folder"""
        try:
            uploads_path = app.config['UPLOAD_FOLDER']
            exists = os.path.exists(uploads_path)
            
            if exists:
                files = []
                for root, dirs, filenames in os.walk(uploads_path):
                    for filename in filenames:
                        filepath = os.path.join(root, filename)
                        rel_path = os.path.relpath(filepath, uploads_path)
                        files.append({
                            "name": filename,
                            "path": rel_path,
                            "size": os.path.getsize(filepath),
                            "exists": os.path.exists(filepath)
                        })
                
                return jsonify({
                    "success": True,
                    "upload_folder": uploads_path,
                    "folder_exists": exists,
                    "files": files,
                    "total_files": len(files)
                })
            else:
                return jsonify({
                    "success": False,
                    "error": f"Upload folder not found: {uploads_path}"
                }), 404
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

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

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return (
            jsonify({
                "success": False, 
                "error": 413, 
                "message": "File too large. Maximum size is 2MB"
            }),
            413,
        )

    @app.route("/api/test-db")
    def test_db():
        try:
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