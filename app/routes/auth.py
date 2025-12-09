import random
import string
from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Guardian, OTP
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from app.utils.email_service import send_otp_email
from flask_jwt_extended import decode_token
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_jwt_extended import get_jwt
from app.utils.password_email_service import send_password_reset_email
from app.utils.serializer import model_to_dict
from datetime import datetime, timedelta, timezone
from app.utils.password_email_service import send_password_reset_email
from app.utils.serializer import model_to_dict



auth_bp = Blueprint('auth', __name__)



# correct
def generate_otp(length=6):
    """Generate a random numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def check_otp_rate_limit(email):
    """
    Check if user has exceeded OTP request limits
    """
    # Count OTP requests in the last hour
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    recent_otps = OTP.query.filter(
        OTP.email == email,
        OTP.created_at >= one_hour_ago
    ).count()
    
    # Limit to 3 OTP requests per hour
    return recent_otps < 3

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return error_response("Email is required", 400)

        # Check rate limit
        if not check_otp_rate_limit(email):
            return error_response("Too many OTP requests. Please try again later.", 429)

        # Generate OTP
        otp_code = generate_otp()
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)

        # Store OTP in database
        otp_record = OTP(
            email=email,
            otp_code=otp_code,
            expires_at=expiration_time,
            is_used=False
        )

        db.session.add(otp_record)
        db.session.commit()

        # Send OTP via email
        email_sent = send_otp_email(
            recipient_email=email,
            otp_code=otp_code
        )

        if not email_sent:
            return error_response("Failed to send OTP email", 500)

        return success_response(
            message="OTP sent successfully",
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to send OTP", 500, str(e))

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp_code = data.get('otp_code')

        if not email or not otp_code:
            return error_response("Email and OTP code are required", 400)

        # Find the most recent valid OTP for this email
        otp_record = OTP.query.filter_by(
            email=email,
            is_used=False
        ).order_by(OTP.created_at.desc()).first()

        if not otp_record:
            return error_response("No OTP found for this email. Please request a new OTP.", 400)

        # Check if OTP is expired
        if datetime.now(timezone.utc) > otp_record.expires_at.replace(tzinfo=timezone.utc):
            return error_response("OTP has expired. Please request a new OTP.", 400)

        # Check if OTP matches
        if otp_record.otp_code != otp_code:
            return error_response("Invalid OTP code. Please try again.", 400)

        # Mark OTP as used
        otp_record.is_used = True
        otp_record.used_at = datetime.now(timezone.utc)
        db.session.commit()

        return success_response(
            message="OTP verified successfully",
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response("OTP verification failed", 500, str(e))

@auth_bp.route('/check-credentials', methods=['POST'])
def check_credentials():
    try:
        data = request.get_json()

        # Check if username exists
        if data.get('username'):
            existing_username = Guardian.query.filter_by(username=data['username']).first()
            if existing_username:
                return error_response("Username already exists. Please use another username", 400)

        # Check if email exists
        if data.get('email'):
            existing_email = Guardian.query.filter_by(email=data['email']).first()
            if existing_email:
                return error_response("Email already exists. Please use another email", 400)

        # Check if contact number exists
        if data.get('contact_number'):
            existing_contact = Guardian.query.filter_by(contact_number=data['contact_number']).first()
            if existing_contact:
                return error_response("Contact number already exists. Please use another contact number", 400)

        return success_response(
            message="All credentials are available",
            status_code=200
        )

    except Exception as e:
        return error_response("Credential check failed", 500, str(e))

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Required fields
        required_fields = [
            'username',
            'password',
            'guardian_name',
            'email',
            'contact_number',
            'relationship_to_vip',
            'province',
            'city',
            'barangay',
            'street_address'
        ]

        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)

        # Check if username or email already exists
        if Guardian.query.filter_by(username=data['username']).first():
            return error_response("Username already exists, please use another username", 400)
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
            guardian_image_url=data.get('guardian_image_url')
        )

        # Hash password before saving
        guardian.password = generate_password_hash(data['password'])

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
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return error_response("Username and password required", 400)
        guardian = Guardian.query.filter_by(username=username).first()

        if not guardian or not check_password_hash(guardian.password, password):
            return error_response("Login failed. Please check your email or password and try again.", 401)

        additional_claims = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "role": guardian.role
        }

        user_data = model_to_dict(
            guardian, 
            include_fields=[
                'guardian_id', 
                'username', 
                'guardian_name', 
                'email',
                'contact_number',
                'role',
                'guardian_image_url',
            ]
        )

        response_body, status_code = success_response(
            data=user_data,
            message="Login successful"
        )

        response = make_response(response_body, status_code)

        set_access_cookies(response, create_access_token(identity=str(guardian.guardian_id), additional_claims=additional_claims))
        set_refresh_cookies(response, create_refresh_token(identity=str(guardian.guardian_id)))
        
        return response
    except Exception as e:
       print(f"Login error: {e}")
       return error_response("Login failed", 500, str(e))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        response_body, status_code = success_response(
            data={"message": "Logged out successfully"},
            message="Logged out successfully"
        )
        
        response = make_response(response_body, status_code)
        
        response.set_cookie(
            'access_token',
            value='',
            expires=0,  
            httponly=True,
            secure=True,  
            samesite='None',  
            path='/',
            domain=None 
        )
        
        response.set_cookie(
            'refresh_token',
            value='',
            expires=0,
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
            domain=None
        )
        
        return response
        
    except Exception as e:
        print(f"Logout error: {e}")
        return error_response("Logout failed", 500, str(e))

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  
def refresh():
    try:
        guardian_id = get_jwt_identity()
        guardian = Guardian.query.get(guardian_id)
        if not guardian:
            return error_response("User not found", 404)
        
        additional_claims = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "role": guardian.role
        }
        
        new_access_token = create_access_token(identity=str(guardian.guardian_id), additional_claims=additional_claims)
        
        response_body, status_code = success_response({
            "success": True,
            "message": "Access token refreshed"
        })
        
        response = make_response(response_body, status_code)
        
        set_access_cookies(response, new_access_token)
        
        return response
        
    except Exception as e:
        return error_response("Invalid refresh token", 401, str(e))
    
@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        try:
            guardian_id = get_jwt_identity() 
            guardian = Guardian.query.get(guardian_id)
            if not guardian:
                return error_response("User not found", 404)
            
            jwt_data = get_jwt()
            
            import time
            current_time = time.time()
            expiry_time = jwt_data.get('exp', 0)
            time_left = expiry_time - current_time
            
            return success_response(
                data={
                    "guardian_id": guardian.guardian_id,
                    "token_valid": True,
                    "expires_in": int(time_left) if time_left > 0 else 0, 
                    "expires_at": expiry_time,  
                    "issued_at": jwt_data.get('iat'), 
                    "token_type": jwt_data.get('type', 'access')
                },
                message="Token is valid"
            )
            
        except Exception as e:
            return error_response("Token verification failed", 401, str(e))
            
    except Exception as e:
        print(f"Verify token error: {e}")
        return error_response("Token verification failed", 500, str(e))
    
# Get guardian profile
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
            "created_at": guardian.created_at.isoformat() if guardian.created_at else None,
            "updated_at": guardian.updated_at.isoformat() if guardian.updated_at else None
        }

        return success_response(data=profile_data)

    except Exception as e:
        return error_response("Failed to fetch profile", 500, str(e))


# forgot pass logics
# --------------------------------------------------
# 1. REQUEST OTP
# --------------------------------------------------
@auth_bp.route('/forgot-password/request', methods=['POST'])
def forgot_password_request():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"message": "Email is required"}), 400

        # Check if user exists
        user = Guardian.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Email not found"}), 404

        # Generate OTP (6 digits)
        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        # Save OTP to database
        otp = OTP(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )

        db.session.add(otp)
        db.session.commit()

        # Send email
        send_password_reset_email(email, otp_code, user.guardian_name)

        return jsonify({"message": "OTP sent to email"}), 200

    except Exception as e:
        print("Forgot password error:", str(e))
        return jsonify({"message": "Internal server error"}), 500


# --------------------------------------------------
# 2. VERIFY OTP
# --------------------------------------------------
@auth_bp.route('/forgot-password/verify', methods=['POST'])
def verify_forgot_password_otp():
    data = request.get_json()
    email = data.get('email')
    otp_code = data.get('otp_code')

    if not email or not otp_code:
        return jsonify({"success": False, "message": "Email and OTP are required"}), 400

    otp = OTP.query.filter_by(
        email=email,
        otp_code=otp_code,
        is_used=False
    ).first()

    if not otp:
        return jsonify({"success": False, "message": "Invalid OTP"}), 400

    # --- FIX STARTS HERE ---
    expires_at = otp.expires_at

    # Convert to timezone-aware if naive
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    # Compare safely
    if datetime.now(timezone.utc) > expires_at:
        return jsonify({"success": False, "message": "OTP expired"}), 400
    # --- FIX ENDS HERE ---

    # Mark OTP as used
    otp.is_used = True
    otp.used_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"success": True, "message": "OTP verified"}), 200



# --------------------------------------------------
# 3. RESET PASSWORD
# --------------------------------------------------
@auth_bp.route('/forgot-password/reset', methods=['POST'])
def reset_forgot_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({"message": "Email and new password are required"}), 400

    user = Guardian.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Update password
    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200