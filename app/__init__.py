from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv 
from datetime import timedelta
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # print("SECRET_KEY:", os.environ.get('SECRET_KEY'))
    # print("DATABASE_URL:", os.environ.get('DATABASE_URL'))
    # print("JWT_SECRET_KEY:", os.environ.get('JWT_SECRET_KEY'))

    load_dotenv()
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://<user>:<password>@<host>:<port>/<database>'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-here')
    # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions
    db.init_app(app)
    # jwt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.vip import vip_bp
    from app.routes.guardian import guardian_bp
    from app.routes.location import location_bp
    from app.routes.reminders import reminders_bp
    from app.routes.alerts import alerts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(vip_bp, url_prefix='/api/vip')
    app.register_blueprint(guardian_bp, url_prefix='/api/guardian')
    app.register_blueprint(location_bp, url_prefix='/api/location')
    app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
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
    
    return app