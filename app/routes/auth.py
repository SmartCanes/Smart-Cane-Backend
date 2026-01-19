from datetime import datetime, timedelta, timezone
import random
import string
from datetime import datetime, timedelta, timezone

from itsdangerous import BadSignature, SignatureExpired
from app.routes.device import verify_guardian_invite_token
from app.utils.auth import guardian_required, guardian_with_device_required
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from sqlalchemy import or_
from app import db
from app.models import Device, DeviceGuardian, Guardian, OTP, GuardianInvitation, LoginAttempt
from app.utils.responses import success_response, error_response
from app.utils.email_service import send_otp_email
from app import limiter
from flask_jwt_extended import decode_token
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_jwt_extended import get_jwt
from app.utils.password_email_service import send_password_reset_email
from app.utils.serializer import model_to_dict
from datetime import datetime, timedelta, timezone
from app.utils.password_email_service import send_password_reset_email
from app.utils.serializer import model_to_dict

# Add these imports at the top of auth.py if not already present
from flask import request, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone
import uuid


auth_bp = Blueprint("auth", __name__)


# correct
def generate_otp(length=6):
    """Generate a random numeric OTP"""
    return "".join(random.choices(string.digits, k=length))


def check_otp_rate_limit(email, purpose="general"):
    """
    Check if user has exceeded OTP request limits
    """
    # Count OTP requests in the last hour
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    recent_otps = OTP.query.filter(
        OTP.email == email, OTP.purpose == purpose, OTP.created_at >= one_hour_ago
    ).count()

    # Limit to 3 OTP requests per hour
    return recent_otps < 3


@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    try:
        data = request.get_json()
        email = data.get("email")
        purpose = data.get("purpose", "general")

        if not email:
            return error_response("Email is required", 400)

        # Check rate limit
        if not check_otp_rate_limit(email, purpose):
            return error_response("Too many OTP requests. Please try again later.", 429)

        # Generate OTP
        otp_code = generate_otp()
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)

        # Store OTP in database
        otp_record = OTP(
            email=email,
            otp_code=otp_code,
            expires_at=expiration_time,
            is_used=False,
            purpose=purpose,
        )

        db.session.add(otp_record)
        db.session.commit()

        # Send OTP via email
        email_sent = send_otp_email(recipient_email=email, otp_code=otp_code)

        if not email_sent:
            return error_response("Failed to send OTP email", 500)

        return success_response(message="OTP sent successfully", status_code=200)

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to send OTP", 500, str(e))


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get("email")
        otp_code = data.get("otp_code")
        purpose = data.get("purpose", "general")

        if not email or not otp_code:
            return error_response("Email and OTP code are required", 400)

        # Find the most recent valid OTP for this email
        otp_record = (
            OTP.query.filter_by(email=email, is_used=False, purpose=purpose)
            .order_by(OTP.created_at.desc())
            .first()
        )

        if not otp_record:
            return error_response(
                "No OTP found for this email. Please request a new OTP.", 400
            )

        # Check if OTP is expired
        if datetime.now(timezone.utc) > otp_record.expires_at.replace(
            tzinfo=timezone.utc
        ):
            return error_response("OTP has expired. Please request a new OTP.", 400)

        # Check if OTP matches
        if otp_record.otp_code != otp_code:
            return error_response("Invalid OTP code. Please try again.", 400)

        # Mark OTP as used
        otp_record.is_used = True
        otp_record.used_at = datetime.now(timezone.utc)
        db.session.commit()

        return success_response(message="OTP verified successfully", status_code=200)

    except Exception as e:
        db.session.rollback()
        return error_response("OTP verification failed", 500, str(e))


def is_login_allowed(username=None, ip_address=None, max_attempts=3, window_minutes=15):
    time_window = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    query = LoginAttempt.query.filter(LoginAttempt.created_at >= time_window)

    if username:
        query = query.filter_by(username=username)
    if ip_address:
        query = query.filter_by(ip_address=ip_address)

    failed_attempts = query.count()
    return failed_attempts < max_attempts


@auth_bp.route("/check-credentials", methods=["POST"])
@limiter.limit("5 per minute")
def check_credentials():
    try:
        data = request.get_json()

        # Check if username exists
        if data.get("username"):
            existing_username = Guardian.query.filter_by(
                username=data["username"]
            ).first()
            if existing_username:
                return error_response(
                    "Username already exists. Please use another username", 400
                )

        # Check if email exists
        if data.get("email"):
            existing_email = Guardian.query.filter_by(email=data["email"]).first()
            if existing_email:
                return error_response(
                    "Email already exists. Please use another email", 400
                )

        # Check if contact number exists
        if data.get("contact_number"):
            existing_contact = Guardian.query.filter_by(
                contact_number=data["contact_number"]
            ).first()
            if existing_contact:
                return error_response(
                    "Contact number already exists. Please use another contact number",
                    400,
                )

        return success_response(
            message="All credentials are available", status_code=200
        )

    except Exception as e:
        return error_response("Credential check failed", 500, str(e))


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}

        required_fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "village",
            "province",
            "city",
            "barangay",
            "street_address",
        ]

        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)

        invite_token = data.get("invite_token")
        invitation = None
        
        if invite_token:
            try:
                verify_guardian_invite_token(invite_token)
            except SignatureExpired:
                return error_response("Invite link has expired", 410)
            except BadSignature:
                return error_response("Invalid invite link", 400)

            invitation = GuardianInvitation.query.filter_by(
                token=invite_token,
                status="pending",
            ).first()

            if not invitation:
                return error_response("Invite is no longer valid", 400)

            if invitation.email != data["email"]:
                return error_response(
                    "Invite email does not match registration email", 400
                )

            if datetime.now(timezone.utc) > invitation.expires_at.replace(
                tzinfo=timezone.utc
            ):
                invitation.status = "expired"
                db.session.commit()
                return error_response("Invite link has expired", 410)

     
        if Guardian.query.filter_by(username=data["username"]).first():
            return error_response(
                "Username already exists, please use another username", 400
            )

        if Guardian.query.filter_by(email=data["email"]).first():
            return error_response("Email already exists", 400)

        guardian = Guardian(
            username=data["username"],
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            email=data["email"],
            contact_number=data.get("contact_number"),
            province=data.get("province"),
            city=data.get("city"),
            barangay=data.get("barangay"),
            village=data.get("village"),
            street_address=data.get("street_address"),
            guardian_image_url=data.get("guardian_image_url"),
        )

        guardian.set_password(data["password"])

        db.session.add(guardian)
        db.session.flush() 

        if invitation:
            device = Device.query.get(invitation.device_id)
            if not device:
                db.session.rollback()
                return error_response("Invited device no longer exists", 404)

            existing_link = DeviceGuardian.query.filter_by(
                guardian_id=guardian.guardian_id,
                device_id=invitation.device_id,
            ).first()

            if not existing_link:
                db.session.add(
                    DeviceGuardian(
                        guardian_id=guardian.guardian_id,
                        device_id=invitation.device_id,
                        assigned_at=datetime.now(timezone.utc),
                    )
                )

            invitation.status = "accepted"
            invitation.accepted_at = datetime.now(timezone.utc)

        db.session.commit()

        additional_claims = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "role": guardian.role,
        }

        response_body, status_code = success_response(
            data={
                "guardian_id": guardian.guardian_id,
                "invite_accepted": bool(invitation),
            },
            message="Guardian registered successfully",
            status_code=201,
        )

        response = make_response(response_body, status_code)

        set_access_cookies(
            response,
            create_access_token(
                identity=str(guardian.guardian_id),
                additional_claims=additional_claims,
            ),
        )
        set_refresh_cookies(
            response,
            create_refresh_token(identity=str(guardian.guardian_id)),
        )

        return response

    except Exception as e:
        db.session.rollback()
        return error_response("Registration failed", 500, str(e))


def get_login_block_info(username, ip_address, window_minutes=30, free_attempts=3):
    LOCKOUTS = [60, 180, 600, 1800]
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)

    # Get recent attempts for username or IP within window
    recent_attempts = (
        LoginAttempt.query.filter(
            or_(
                LoginAttempt.username == username, LoginAttempt.ip_address == ip_address
            ),
            LoginAttempt.created_at >= window_start,
        )
        .order_by(LoginAttempt.created_at.asc())
        .all()
    )

    attempts_count = len(recent_attempts)

    if attempts_count <= free_attempts:
        remaining_attempts = max(0, free_attempts - attempts_count)
        return {
            "allowed": True,
            "remaining_attempts": remaining_attempts,
            "retry_after": 0,
        }

    lockout_index = min(attempts_count - free_attempts - 1, len(LOCKOUTS) - 1)
    lockout_seconds = LOCKOUTS[lockout_index]

    last_attempt_time = recent_attempts[-1].created_at
    if last_attempt_time.tzinfo is None:
        last_attempt_time = last_attempt_time.replace(tzinfo=timezone.utc)

    retry_after = max(
        0,
        int(
            (
                last_attempt_time + timedelta(seconds=lockout_seconds) - now
            ).total_seconds()
        ),
    )

    allowed = retry_after == 0
    remaining_attempts = 0

    return {
        "allowed": allowed,
        "remaining_attempts": remaining_attempts,
        "retry_after": retry_after,
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        identifier = data.get("identifier")
        password = data.get("password")
        ip_addr = request.remote_addr

        if not identifier or not password:
            return error_response("Email/Username and password required", 400)

        identifier = identifier.strip().lower()

        # Determine identifier type
        is_email = "@" in identifier

        # Resolve guardian FIRST
        guardian = (
            Guardian.query.filter_by(email=identifier).first()
            if is_email
            else Guardian.query.filter_by(username=identifier).first()
        )

        # Use username for lockout tracking (consistent)
        lockout_username = guardian.username if guardian else identifier

        # Progressive lockout
        block_info = get_login_block_info(username=lockout_username, ip_address=ip_addr)
        if not block_info["allowed"]:
            return error_response(
                f"Too many failed login attempts. Try again in {block_info['retry_after']} seconds.",
                429,
            )

        # Invalid credentials
        if not guardian or not guardian.check_password(password):
            attempt = LoginAttempt(username=lockout_username, ip_address=ip_addr)
            db.session.add(attempt)
            db.session.commit()
            return error_response(
                "Login failed. Please check your email/username or password.", 401
            )

        # Clear failed attempts on success
        LoginAttempt.query.filter(
            or_(
                LoginAttempt.username == guardian.username,
                LoginAttempt.ip_address == ip_addr,
            )
        ).delete()
        db.session.commit()

        guardian_device = DeviceGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).first()
        device_registered = bool(guardian_device)

        additional_claims = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "role": guardian.role,
        }

        user_data = model_to_dict(
            guardian,
            include_fields=[
                "guardian_id",
                "username",
                "first_name",
                "middle_name",
                "last_name",
                "email",
                "contact_number",
                "role",
                "province",
                "city",
                "barangay",
                "village",
                "street_address",
                "guardian_image_url",
            ],
        )

        response_body, status_code = success_response(
            data={**user_data, "device_registered": device_registered},  # type: ignore
            message="Login successful",
        )

        response = make_response(response_body, status_code)
        set_access_cookies(
            response,
            create_access_token(
                identity=str(guardian.guardian_id), additional_claims=additional_claims
            ),
        )
        set_refresh_cookies(
            response, create_refresh_token(identity=str(guardian.guardian_id))
        )

        return response

    except Exception as e:
        print(f"Login error: {e}")
        return error_response("Login failed", 500)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    try:
        response_body, status_code = success_response(
            data={"message": "Logged out successfully"},
            message="Logged out successfully",
        )

        response = make_response(response_body, status_code)

        response.set_cookie(
            "access_token",
            value="",
            expires=0,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            domain=None,
        )

        response.set_cookie(
            "refresh_token",
            value="",
            expires=0,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            domain=None,
        )

        return response

    except Exception as e:
        print(f"Logout error: {e}")
        return error_response("Logout failed", 500, str(e))


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        guardian_id = get_jwt_identity()
        guardian = Guardian.query.get(guardian_id)
        if not guardian:
            return error_response("Invalid refresh token", 401)

        additional_claims = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "role": guardian.role,
        }

        new_access_token = create_access_token(
            identity=str(guardian.guardian_id), additional_claims=additional_claims
        )

        print(f"[TOKEN REFRESH] Guardian {guardian.username} ({guardian.guardian_id}) at {datetime.now(timezone.utc)}")

        response_body, status_code = success_response(
            {"success": True, "message": "Access token refreshed"}
        )

        response = make_response(response_body, status_code)

        set_access_cookies(response, new_access_token)

        return response

    except Exception as e:
        return error_response("Invalid refresh token", 401, str(e))


@auth_bp.route("/verify-token", methods=["GET"])
@guardian_required
@guardian_with_device_required
def verify_token(guardian):
    try:
        try:
            jwt_data = get_jwt()

            import time

            current_time = time.time()
            expiry_time = jwt_data.get("exp", 0)
            time_left = expiry_time - current_time

            return success_response(
                data={
                    "guardian_id": guardian.guardian_id,
                    "token_valid": True,
                    "expires_in": int(time_left) if time_left > 0 else 0,
                    "expires_at": expiry_time,
                    "issued_at": jwt_data.get("iat"),
                    "token_type": jwt_data.get("type", "access"),
                },
                message="Token is valid",
            )

        except Exception as e:
            return error_response("Token verification failed", 401, str(e))

    except Exception as e:
        print(f"Verify token error: {e}")
        return error_response("Token verification failed", 500, str(e))


# Request OTP for email change
@auth_bp.route("/profile/change-email/request", methods=["POST"])
@guardian_required
def request_email_change(guardian):
    data = request.get_json()
    new_email = data.get("new_email")

    if not new_email:
        return error_response("New email is required", 400)

    # guardian is already available here
    existing_email = Guardian.query.filter_by(email=new_email).first()
    if existing_email and existing_email.guardian_id != guardian.guardian_id:
        return error_response("Email already exists. Please use another email", 400)

    if not check_otp_rate_limit(new_email, "email_change"):
        return error_response("Too many OTP requests. Please try again later.", 429)

    otp_code = generate_otp()
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    otp_record = OTP(
        email=new_email,
        otp_code=otp_code,
        expires_at=expiration_time,
        is_used=False,
        purpose="email_change",
    )

    db.session.add(otp_record)
    db.session.commit()

    email_sent = send_otp_email(recipient_email=new_email, otp_code=otp_code)
    if not email_sent:
        return error_response("Failed to send OTP email", 500)

    return success_response(message="OTP sent to new email address", status_code=200)


@auth_bp.route("/profile/change-email/verify", methods=["POST"])
@guardian_required
def verify_email_change(guardian):
    data = request.get_json()
    new_email = data.get("new_email")
    otp_code = data.get("otp_code")

    if not new_email or not otp_code:
        return error_response("New email and OTP code are required", 400)

    otp_record = OTP.query.filter_by(
        email=new_email, otp_code=otp_code, is_used=False, purpose="email_change"
    ).first()

    if not otp_record:
        return error_response("Invalid OTP for email change", 400)

    if datetime.now(timezone.utc) > otp_record.expires_at.replace(tzinfo=timezone.utc):
        return error_response("OTP has expired. Please request a new OTP.", 400)

    existing_email = Guardian.query.filter_by(email=new_email).first()
    if existing_email and existing_email.guardian_id != guardian.guardian_id:
        return error_response("Email already exists. Please use another email", 400)

    old_email = guardian.email
    guardian.email = new_email

    otp_record.is_used = True
    otp_record.used_at = datetime.now(timezone.utc)

    db.session.commit()

    return success_response(
        message="Email updated successfully",
        data={"old_email": old_email, "new_email": new_email},
        status_code=200,
    )


# forgot pass logics
# --------------------------------------------------
# 1. REQUEST OTP
# --------------------------------------------------
@auth_bp.route("/forgot-password/request", methods=["POST"])
def forgot_password_request():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return error_response("Email is required", 400)

        user = Guardian.query.filter_by(email=email).first()
        if not user:
            return error_response("Email not found", 404)

        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        # Save OTP to database
        otp = OTP(email=email, otp_code=otp_code, expires_at=expires_at)

        db.session.add(otp)
        db.session.commit()

        send_password_reset_email(email, otp_code, user.guardian_name)

        return success_response(message="OTP sent to email", status_code=200)

    except Exception as e:
        print("Forgot password error:", str(e))
        return error_response("Failed to process password reset request", 500, str(e))


# --------------------------------------------------
# 2. VERIFY OTP
# --------------------------------------------------
@auth_bp.route("/forgot-password/verify", methods=["POST"])
def verify_forgot_password_otp():
    try:
        data = request.get_json()
        email = data.get("email")
        otp_code = data.get("otp_code")

        if not email or not otp_code:
            return error_response("Email and OTP are required", 400)

        otp = OTP.query.filter_by(
            email=email, otp_code=otp_code, is_used=False, purpose="password_reset"
        ).first()

        if not otp:
            return error_response("Invalid OTP", 400)

        expires_at = otp.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > expires_at:
            return error_response("OTP expired", 400)

        otp.is_used = True
        otp.used_at = datetime.now(timezone.utc)
        db.session.commit()

        return success_response(message="OTP verified", status_code=200)

    except Exception as e:
        db.session.rollback()
        return error_response("OTP verification failed", 500, str(e))


# --------------------------------------------------
# 3. RESET PASSWORD
# --------------------------------------------------


@auth_bp.route("/forgot-password/reset", methods=["POST"])
def reset_forgot_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not new_password:
        return error_response("Email and new password are required", 400)
    user = Guardian.query.filter_by(email=email).first()

    if not user:
        return error_response("User not found", 404)

    user.set_password(new_password)

    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200
