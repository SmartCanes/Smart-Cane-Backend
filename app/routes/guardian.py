from flask import Blueprint, request, current_app
from app import db
from app.models import Guardian, VIPGuardian, VIP
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone
import uuid

from app.utils.serializer import model_to_dict

guardian_bp = Blueprint("guardian", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@guardian_bp.route("/profile/image", methods=["POST"])
@guardian_required
def upload_profile_image(guardian):
    """Upload profile image for current logged-in guardian"""
    try:
        print(f"Starting image upload for guardian: {guardian.guardian_id}")

        if "image" not in request.files:
            return error_response("No image file provided", 400)

        file = request.files["image"]

        if file.filename == "":
            return error_response("No selected file", 400)

        if not allowed_file(file.filename):
            return error_response(
                "File type not allowed. Only PNG, JPG, JPEG, GIF, WEBP are allowed", 400
            )

        print(f"File received: {file.filename}, Size: {file.content_length} bytes")

        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit(".", 1)[1].lower()
        new_filename = (
            f"guardian_{guardian.guardian_id}_{timestamp}_{unique_id}.{file_extension}"
        )

        print(f"Generated filename: {new_filename}")

        # Save file with debugging
        upload_folder = current_app.config["UPLOAD_FOLDER"]

        upload_path = os.path.join(upload_folder, "profile_pics")

        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, new_filename)

        file.save(file_path)

        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        else:
            return error_response("Failed to save image file", 500)

        if guardian.guardian_image_url:
            old_image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], guardian.guardian_image_url
            )
            print(f"🗑️ Old image path to delete: {old_image_path}")
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception as delete_error:
                    print(f"⚠️ Could not delete old image: {delete_error}")
                    pass

        relative_path = f"profile_pics/{new_filename}"
        guardian.guardian_image_url = relative_path
        guardian.updated_at = datetime.now(timezone.utc)

        db.session.commit()

        base_url = request.host_url.rstrip("/")
        image_url = f"{base_url}/uploads/{relative_path}"

        return success_response(
            data={
                "image_url": image_url,
                "relative_path": relative_path,
                "avatar": image_url,
                "guardian_image_url": image_url,
            },
            message="Profile image uploaded successfully",
        )

    except Exception as e:
        db.session.rollback()
        print(f"IMAGE UPLOAD ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        return error_response("Failed to upload image", 500, str(e))


@guardian_bp.route("/profile", methods=["GET"])
@guardian_required
def get_profile(guardian):
    try:
        profile_data = {
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "first_name": guardian.first_name,
            "middle_name": guardian.middle_name,
            "last_name": guardian.last_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "street_address": guardian.street_address,
            "guardian_image_url": guardian.guardian_image_url,
            "created_at": (
                guardian.created_at.isoformat() if guardian.created_at else None
            ),
            "updated_at": (
                guardian.updated_at.isoformat() if guardian.updated_at else None
            ),
        }

        return success_response(data=profile_data)

    except Exception as e:
        return error_response("Failed to fetch profile", 500, str(e))


@guardian_bp.route("/profile", methods=["PUT"])
@guardian_required
def update_my_profile(guardian):
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response("Invalid JSON payload", 400)

        if "email" in data and data["email"] != guardian.email:
            existing_guardian = Guardian.query.filter_by(email=data["email"]).first()
            if existing_guardian:
                return error_response("Email already exists", 400)

        if "username" in data and data["username"] != guardian.username:
            existing_guardian = Guardian.query.filter_by(
                username=data["username"]
            ).first()
            if existing_guardian:
                return error_response("Username already exists", 400)

        allowed_fields = [
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "contact_number",
            "province",
            "city",
            "barangay",
            "village",
            "street_address",
        ]

        nullable_fields = ["middle_name", "guardian_image_url"]

        for field in allowed_fields:
            if field in data:
                value = data[field]
                if field in nullable_fields and value == "":
                    value = None
                setattr(guardian, field, value)

            # Update password if provided
            if "password" in data and data["password"]:
                guardian.set_password(data["password"])

            if "guardian_image_url" in data:
                if guardian.guardian_image_url and not data["guardian_image_url"]:
                    old_path = os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        guardian.guardian_image_url.lstrip("/"),
                    )
                    if os.path.exists(old_path):
                        os.remove(old_path)

                guardian.guardian_image_url = data["guardian_image_url"]

        db.session.commit()

        return success_response(
            data=model_to_dict(guardian), message="Profile updated successfully"
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update profile", 500, str(e))


@guardian_bp.route("", methods=["GET"])
@guardian_required
def get_guardians_by_vip(guardian):
    try:
        vip_id = request.args.get("vip_id", type=int)

        if not vip_id:
            return error_response("VIP ID is required", 400)

        guardians = Guardian.query.filter_by(vip_id=vip_id).all()

        guardian_list = []
        for g in guardians:
            guardian_image_url = None
            if g.guardian_image_url:
                base_url = request.host_url.rstrip("/")
                guardian_image_url = f"{base_url}/uploads/{g.guardian_image_url}"

            guardian_list.append(
                {
                    "guardian_id": g.guardian_id,
                    "username": g.username,
                    "email": g.email,
                    "first_name": g.first_name,
                    "middle_name": g.middle_name,
                    "last_name": g.last_name,
                    "contact_number": g.contact_number,
                    "relationship_to_vip": g.relationship_to_vip,
                    "guardian_image_url": guardian_image_url,  # Full URL
                    "created_at": g.created_at.isoformat() if g.created_at else None,
                }
            )

        return success_response(data=guardian_list)

    except Exception as e:
        return error_response("Failed to fetch guardians", 500, str(e))


@guardian_bp.route("/<int:guardian_id>", methods=["GET"])
@guardian_required
def get_guardian(guardian, guardian_id):
    try:
        guardian_data = Guardian.query.get(guardian_id)

        if not guardian_data:
            return error_response("Guardian not found", 404)

        guardian_image_url = None
        if guardian_data.guardian_image_url:
            base_url = request.host_url.rstrip("/")
            guardian_image_url = (
                f"{base_url}/uploads/{guardian_data.guardian_image_url}"
            )

        guardian_info = {
            "guardian_id": guardian_data.guardian_id,
            "username": guardian_data.username,
            "first_name": guardian_data.first_name,
            "middle_name": guardian_data.middle_name,
            "last_name": guardian_data.last_name,
            "email": guardian_data.email,
            "contact_number": guardian_data.contact_number,
            "relationship_to_vip": guardian_data.relationship_to_vip,
            "province": guardian_data.province,
            "city": guardian_data.city,
            "barangay": guardian_data.barangay,
            "street_address": guardian_data.street_address,
            "guardian_image_url": guardian_image_url,  # Full URL
            "created_at": (
                guardian_data.created_at.isoformat()
                if guardian_data.created_at
                else None
            ),
        }

        return success_response(data=guardian_info)

    except Exception as e:
        return error_response("Failed to fetch guardian", 500, str(e))


@guardian_bp.route("/<int:guardian_id>", methods=["PUT"])
@guardian_required
def update_guardian(guardian, guardian_id):
    try:
        if guardian.guardian_id != guardian_id:
            return error_response("Unauthorized to update this profile", 403)

        data = request.get_json()

        if data.get("email"):
            existing_guardian = Guardian.query.filter(
                Guardian.email == data["email"], Guardian.guardian_id != guardian_id
            ).first()
            if existing_guardian:
                return error_response("Email already exists", 400)

        if data.get("username"):
            existing_guardian = Guardian.query.filter(
                Guardian.username == data["username"],
                Guardian.guardian_id != guardian_id,
            ).first()
            if existing_guardian:
                return error_response("Username already exists", 400)

        updatable_fields = ["role", "nickname"]

        for field in updatable_fields:
            if field in data:
                setattr(guardian, field, data[field])

        if data.get("password"):
            guardian.set_password(data["password"])

        db.session.commit()

        return success_response(message="Guardian updated successfully")

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update guardian", 500, str(e))
