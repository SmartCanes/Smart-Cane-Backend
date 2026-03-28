import os
import uuid
import bcrypt                                       # ← NEW: pip install bcrypt
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.models import Admin, AdminArchive, OTP     # ← added AdminArchive
from app.utils.admin_email_service import send_admin_otp_email
from datetime import datetime, timezone, timedelta
import random, string

admin_bp = Blueprint("admin", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE_MB   = 2


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def require_super_admin():
    claims = get_jwt()
    if claims.get("role") != "super_admin":
        return jsonify({"message": "Access denied. Super admin only."}), 403
    return None


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of the plain-text password."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder() -> str:
    root: str = current_app.root_path or ""
    folder = os.path.join(root, "..", "static", "uploads", "profiles")
    os.makedirs(folder, exist_ok=True)
    return os.path.abspath(folder)


# ═════════════════════════════════════════════════════════════════════════════
#  ADMIN MANAGEMENT  (super_admin only)
# ═════════════════════════════════════════════════════════════════════════════

@admin_bp.route("/", methods=["GET"])
@jwt_required()
def list_admins():
    """All authenticated admins can view the list."""
    admins = Admin.query.order_by(Admin.created_at.desc()).all()
    return jsonify([{
        "admin_id":          a.admin_id,
        "username":          a.username,
        "email":             a.email,
        "first_name":        a.first_name,
        "middle_name":       a.middle_name,
        "last_name":         a.last_name,
        "contact_number":    a.contact_number,
        "province":          a.province,
        "city":              a.city,
        "barangay":          a.barangay,
        "street_address":    a.street_address,
        "role":              a.role,
        "is_first_login":    a.is_first_login,
        "profile_image_url": a.profile_image_url,
        "created_at":        a.created_at.isoformat() if a.created_at else None,
    } for a in admins]), 200


@admin_bp.route("/create", methods=["POST"])
@jwt_required()
def create_admin():
    err = require_super_admin()
    if err:
        return err

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Request body must be JSON."}), 400

    for field in ["username", "email", "password", "first_name", "last_name"]:
        if not data.get(field, "").strip():
            return jsonify({"message": f"{field} is required."}), 400

    if Admin.query.filter_by(username=data["username"].strip()).first():
        return jsonify({"message": "Username already exists."}), 409
    if Admin.query.filter_by(email=data["email"].strip()).first():
        return jsonify({"message": "Email already exists."}), 409

    new_admin = Admin(
        username       = data["username"].strip(),
        email          = data["email"].strip(),
        password       = hash_password(data["password"].strip()),  # ← bcrypt hashed
        first_name     = data["first_name"].strip(),
        middle_name    = data.get("middle_name", "").strip() or None,
        last_name      = data["last_name"].strip(),
        contact_number = data.get("contact_number", "").strip() or None,
        province       = data.get("province", "").strip() or None,
        city           = data.get("city", "").strip() or None,
        barangay       = data.get("barangay", "").strip() or None,
        street_address = data.get("street_address", "").strip() or None,
        role           = data.get("role", "admin"),
        is_first_login = True,
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin created successfully.", "admin_id": new_admin.admin_id}), 201


@admin_bp.route("/<int:target_id>/update", methods=["PUT"])
@jwt_required()
def update_admin(target_id):
    """Super-admin updates another admin's details."""
    err = require_super_admin()
    if err:
        return err

    target = Admin.query.get_or_404(target_id)
    data   = request.get_json(silent=True) or {}

    # ── Username uniqueness check ──
    new_username = data.get("username", "").strip()
    if new_username and new_username != target.username:
        clash = Admin.query.filter_by(username=new_username).first()
        if clash and clash.admin_id != target_id:
            return jsonify({"message": "Username already taken."}), 409

    # ── Email uniqueness check ──
    new_email = data.get("email", "").strip()
    if new_email and new_email != target.email:
        clash = Admin.query.filter_by(email=new_email).first()
        if clash and clash.admin_id != target_id:
            return jsonify({"message": "Email already taken."}), 409

    # ── Apply updates ──
    target.first_name     = data.get("first_name",     target.first_name).strip()
    target.middle_name    = data.get("middle_name",     target.middle_name or "").strip() or None
    target.last_name      = data.get("last_name",       target.last_name).strip()
    target.username       = new_username or target.username
    target.email          = new_email    or target.email
    target.contact_number = data.get("contact_number",  target.contact_number or "").strip() or None
    target.province       = data.get("province",        target.province or "").strip() or None
    target.city           = data.get("city",             target.city or "").strip() or None
    target.barangay       = data.get("barangay",         target.barangay or "").strip() or None
    target.street_address = data.get("street_address",   target.street_address or "").strip() or None
    target.role           = data.get("role",             target.role)
    target.updated_at     = datetime.now(timezone.utc)

    # ── Optional password reset ──
    new_password = data.get("password", "").strip()
    if new_password:
        target.password       = hash_password(new_password)
        target.is_first_login = True    # force the admin to go through first-login flow again

    db.session.commit()
    return jsonify({"message": "Admin updated successfully."}), 200


@admin_bp.route("/<int:target_id>/delete", methods=["DELETE"])
@jwt_required()
def delete_admin(target_id):
    """
    Super-admin deletes an admin:
      1. Copy the record to admin_archive_tbl
      2. Delete from admin_tbl
    """
    err = require_super_admin()
    if err:
        return err

    caller_id = int(get_jwt_identity())

    # Prevent super-admin from deleting themselves
    if caller_id == target_id:
        return jsonify({"message": "You cannot delete your own account."}), 400

    target = Admin.query.get_or_404(target_id)

    # ── Archive first ──
    archive = AdminArchive(
        admin_id            = target.admin_id,
        username            = target.username,
        email               = target.email,
        password            = target.password,
        first_name          = target.first_name,
        middle_name         = target.middle_name,
        last_name           = target.last_name,
        contact_number      = target.contact_number,
        province            = target.province,
        city                = target.city,
        barangay            = target.barangay,
        street_address      = target.street_address,
        role                = target.role,
        profile_image_url   = target.profile_image_url,
        original_created_at = target.created_at,
        archived_at         = datetime.now(timezone.utc),
        archived_by         = caller_id,
    )
    db.session.add(archive)

    # ── Then delete ──
    db.session.delete(target)
    db.session.commit()

    return jsonify({"message": "Admin deleted and archived successfully."}), 200


# ═════════════════════════════════════════════════════════════════════════════
#  FIRST LOGIN FLOW
# ═════════════════════════════════════════════════════════════════════════════

@admin_bp.route("/request-otp", methods=["POST"])
def request_otp():
    data  = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"message": "Email is required."}), 400
    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({"message": "If that email exists, an OTP has been sent."}), 200

    OTP.query.filter_by(email=email, purpose="first_login", is_used=False).update({"is_used": True})
    db.session.commit()

    code       = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp = OTP(email=email, otp_code=code, is_used=False, expires_at=expires_at, purpose="first_login")
    db.session.add(otp)
    db.session.commit()

    send_admin_otp_email(recipient_email=email, otp_code=code, admin_name=admin.first_name)
    return jsonify({"message": "OTP sent to email."}), 200


@admin_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data     = request.get_json(silent=True) or {}
    email    = data.get("email",    "").strip()
    otp_code = data.get("otp_code", "").strip()
    if not email or not otp_code:
        return jsonify({"message": "email and otp_code are required."}), 400

    otp = OTP.query.filter_by(email=email, otp_code=otp_code, is_used=False, purpose="first_login").first()
    if not otp:
        return jsonify({"message": "Invalid OTP."}), 400
    if datetime.now(timezone.utc) > otp.expires_at.replace(tzinfo=timezone.utc):
        return jsonify({"message": "OTP has expired. Please request a new one."}), 400

    otp.is_used = True
    otp.used_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"message": "OTP verified. You may now change your credentials."}), 200


@admin_bp.route("/change-credentials", methods=["POST"])
def change_credentials():
    data         = request.get_json(silent=True) or {}
    email        = data.get("email",        "").strip()
    new_username = data.get("new_username", "").strip()
    new_password = data.get("new_password", "").strip()
    if not email or not new_username or not new_password:
        return jsonify({"message": "email, new_username, and new_password are required."}), 400

    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({"message": "Admin not found."}), 404

    existing = Admin.query.filter_by(username=new_username).first()
    if existing and existing.admin_id != admin.admin_id:
        return jsonify({"message": "Username already taken."}), 409

    admin.username       = new_username
    admin.password       = hash_password(new_password)     # ← bcrypt hashed
    admin.is_first_login = False
    admin.updated_at     = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"message": "Credentials updated successfully."}), 200


# ═════════════════════════════════════════════════════════════════════════════
#  PROFILE  (logged-in admin's own profile)
# ═════════════════════════════════════════════════════════════════════════════

@admin_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    admin_id = int(get_jwt_identity())
    admin    = Admin.query.get_or_404(admin_id)
    return jsonify({
        "admin_id":          admin.admin_id,
        "username":          admin.username,
        "email":             admin.email,
        "first_name":        admin.first_name,
        "middle_name":       admin.middle_name,
        "last_name":         admin.last_name,
        "contact_number":    admin.contact_number,
        "province":          admin.province,
        "city":              admin.city,
        "barangay":          admin.barangay,
        "street_address":    admin.street_address,
        "role":              admin.role,
        "profile_image_url": admin.profile_image_url,
        "created_at":        admin.created_at.isoformat() if admin.created_at else None,
    }), 200


@admin_bp.route("/profile/update", methods=["PUT"])
@jwt_required()
def update_profile():
    admin_id = int(get_jwt_identity())
    admin    = Admin.query.get_or_404(admin_id)
    data     = request.get_json(silent=True) or {}

    new_username = data.get("username", "").strip()
    if new_username and new_username != admin.username:
        existing = Admin.query.filter_by(username=new_username).first()
        if existing and existing.admin_id != admin_id:
            return jsonify({"message": "Username already taken."}), 409

    admin.first_name     = data.get("first_name",     admin.first_name).strip()
    admin.middle_name    = data.get("middle_name",     admin.middle_name or "").strip() or None
    admin.last_name      = data.get("last_name",       admin.last_name).strip()
    admin.username       = new_username or admin.username
    admin.contact_number = data.get("contact_number",  admin.contact_number or "").strip() or None
    admin.province       = data.get("province",        admin.province or "").strip() or None
    admin.city           = data.get("city",             admin.city or "").strip() or None
    admin.barangay       = data.get("barangay",         admin.barangay or "").strip() or None
    admin.street_address = data.get("street_address",   admin.street_address or "").strip() or None
    admin.updated_at     = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully."}), 200


@admin_bp.route("/profile/upload-image", methods=["POST"])
@jwt_required()
def upload_image():
    admin_id = int(get_jwt_identity())
    admin    = Admin.query.get_or_404(admin_id)

    if "image" not in request.files:
        return jsonify({"message": "No image file provided."}), 400
    file = request.files["image"]
    if not file.filename:
        return jsonify({"message": "No file selected."}), 400
    if not allowed_file(file.filename):
        return jsonify({"message": "Only PNG, JPG, JPEG, and WEBP files are allowed."}), 400

    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > MAX_FILE_SIZE_MB:
        return jsonify({"message": f"Image must be under {MAX_FILE_SIZE_MB}MB."}), 400

    if admin.profile_image_url:
        old_filename = admin.profile_image_url.split("/")[-1]
        old_path     = os.path.join(get_upload_folder(), old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    ext          = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    new_filename = f"admin_{admin_id}_{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(get_upload_folder(), new_filename))

    base_url  = request.host_url.rstrip("/")
    image_url = f"{base_url}/static/uploads/profiles/{new_filename}"

    admin.profile_image_url = image_url
    admin.updated_at        = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Profile image uploaded successfully.", "profile_image_url": image_url}), 200


@admin_bp.route("/profile/remove-image", methods=["DELETE"])
@jwt_required()
def remove_image():
    admin_id = int(get_jwt_identity())
    admin    = Admin.query.get_or_404(admin_id)

    if admin.profile_image_url:
        old_filename = admin.profile_image_url.split("/")[-1]
        old_path     = os.path.join(get_upload_folder(), old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)
        admin.profile_image_url = None
        admin.updated_at        = datetime.now(timezone.utc)
        db.session.commit()

    return jsonify({"message": "Profile image removed."}), 200


@admin_bp.route("/profile/request-email-otp", methods=["POST"])
@jwt_required()
def request_email_otp():
    admin_id  = int(get_jwt_identity())
    admin     = Admin.query.get_or_404(admin_id)
    data      = request.get_json(silent=True) or {}
    new_email = data.get("new_email", "").strip()

    if not new_email:
        return jsonify({"message": "new_email is required."}), 400
    if new_email == admin.email:
        return jsonify({"message": "New email must be different from current email."}), 400

    existing = Admin.query.filter_by(email=new_email).first()
    if existing and existing.admin_id != admin_id:
        return jsonify({"message": "Email already in use by another account."}), 409

    OTP.query.filter_by(email=new_email, purpose="email_change", is_used=False).update({"is_used": True})
    db.session.commit()

    code       = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp = OTP(email=new_email, otp_code=code, is_used=False, expires_at=expires_at, purpose="email_change")
    db.session.add(otp)
    db.session.commit()

    send_admin_otp_email(recipient_email=new_email, otp_code=code, admin_name=admin.first_name)
    return jsonify({"message": "OTP sent to new email."}), 200


@admin_bp.route("/profile/verify-email-otp", methods=["POST"])
@jwt_required()
def verify_email_otp():
    admin_id  = int(get_jwt_identity())
    admin     = Admin.query.get_or_404(admin_id)
    data      = request.get_json(silent=True) or {}
    new_email = data.get("new_email", "").strip()
    otp_code  = data.get("otp_code",  "").strip()

    if not new_email or not otp_code:
        return jsonify({"message": "new_email and otp_code are required."}), 400

    otp = OTP.query.filter_by(email=new_email, otp_code=otp_code, is_used=False, purpose="email_change").first()
    if not otp:
        return jsonify({"message": "Invalid OTP."}), 400
    if datetime.now(timezone.utc) > otp.expires_at.replace(tzinfo=timezone.utc):
        return jsonify({"message": "OTP has expired. Please request a new one."}), 400

    otp.is_used      = True
    otp.used_at      = datetime.now(timezone.utc)
    admin.email      = new_email
    admin.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Email updated successfully."}), 200