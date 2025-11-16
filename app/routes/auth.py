from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import Guardian
from app.utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['username', 'password', 'guardian_name', 'email', 'vip_id']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)
        
        # Check if username or email already exists
        if Guardian.query.filter_by(username=data['username']).first():
            return error_response("Username already exists", 400)
        
        if Guardian.query.filter_by(email=data['email']).first():
            return error_response("Email already exists", 400)
        
        # Create new guardian
        guardian = Guardian(
            username=data['username'],
            guardian_name=data['guardian_name'],
            email=data['email'],
            contact_number=data.get('contact_number'),
            relationship_to_vip=data.get('relationship_to_vip'),
            province=data.get('province'),
            city=data.get('city'),
            barangay=data.get('barangay'),
            street_address=data.get('street_address'),
            vip_id=data['vip_id'],
            guardian_image_url=data.get('guardian_image_url')
        )
        guardian.set_password(data['password'])
        
        db.session.add(guardian)
        db.session.commit()
        
        return success_response(
            data={"guardian_id": guardian.guardian_id},
            message="Guardian registered successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Registration failed", 500, str(e))

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return error_response("Username and password required", 400)
        
        guardian = Guardian.query.filter_by(username=data['username']).first()
        
        if not guardian or not guardian.check_password(data['password']):
            return error_response("Invalid credentials", 401)
        
        access_token = create_access_token(identity=guardian.guardian_id)
        
        return success_response(data={
            "access_token": access_token,
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "guardian_name": guardian.guardian_name
        }, message="Login successful")
        
    except Exception as e:
        return error_response("Login failed", 500, str(e))

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        guardian_id = get_jwt_identity()
        guardian = Guardian.query.get(guardian_id)
        
        if not guardian:
            return error_response("Guardian not found", 404)
        
        profile_data = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "guardian_name": guardian.guardian_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "relationship_to_vip": guardian.relationship_to_vip,
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "street_address": guardian.street_address,
            "guardian_image_url": guardian.guardian_image_url,
            "vip_id": guardian.vip_id,
            "created_at": guardian.created_at.isoformat() if guardian.created_at else None
        }
        
        return success_response(data=profile_data)
        
    except Exception as e:
        return error_response("Failed to fetch profile", 500, str(e))