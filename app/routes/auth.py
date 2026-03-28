import bcrypt                                        # ← pip install bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import Admin, LoginAttempt
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__)


def _record_attempt(username, ip):
    """Save every login attempt to the DB for audit purposes."""
    attempt = LoginAttempt(
        username=username,
        ip_address=ip,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(attempt)
    db.session.commit()


def _check_password(stored: str, plain: str) -> bool:
    """
    Accepts both bcrypt hashes (new) and legacy plain-text passwords (old rows).
    Once all passwords are migrated to bcrypt you can remove the plain-text branch.
    """
    if stored.startswith(("$2b$", "$2a$")):
        return bcrypt.checkpw(plain.encode("utf-8"), stored.encode("utf-8"))
    # Legacy plain-text fallback — remove this after migration
    return stored == plain


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Request body must be JSON."}), 400

    identifier = (data.get("identifier") or "").strip()
    password   = (data.get("password")   or "").strip()

    if not identifier or not password:
        return jsonify({"message": "identifier and password are required."}), 400

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    admin = Admin.query.filter(
        (Admin.username == identifier) | (Admin.email == identifier)
    ).first()

    _record_attempt(identifier, ip)

    if admin is None:
        return jsonify({"message": "Invalid credentials."}), 401

    if not _check_password(admin.password, password):
        return jsonify({"message": "Invalid credentials."}), 401

    access_token = create_access_token(
        identity=str(admin.admin_id),
        additional_claims={
            "role":  admin.role,
            "email": admin.email,
            "type":  "admin",
        },
    )

    return jsonify({
        "access_token":   access_token,
        "admin_id":       admin.admin_id,
        "role":           admin.role,
        "first_name":     admin.first_name,
        "last_name":      admin.last_name,
        "email":          admin.email,
        "is_first_login": admin.is_first_login,
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get_or_404(admin_id)

    return jsonify({
        "admin_id":       admin.admin_id,
        "username":       admin.username,
        "email":          admin.email,
        "first_name":     admin.first_name,
        "middle_name":    admin.middle_name,
        "last_name":      admin.last_name,
        "contact_number": admin.contact_number,
        "province":       admin.province,
        "city":           admin.city,
        "barangay":       admin.barangay,
        "street_address": admin.street_address,
        "role":           admin.role,
        "is_first_login": admin.is_first_login,
        "created_at":     admin.created_at.isoformat() if admin.created_at else None,
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully."}), 200