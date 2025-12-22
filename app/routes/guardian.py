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

guardian_bp = Blueprint("guardian", __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@guardian_bp.route("/profile/image", methods=["POST"])
@guardian_required
def upload_profile_image(guardian):
    """Upload profile image for current logged-in guardian"""
    try:
        print(f"Starting image upload for guardian: {guardian.guardian_id}")
        
        if 'image' not in request.files:
            return error_response("No image file provided", 400)
        
        file = request.files['image']
        
        if file.filename == '':
            return error_response("No selected file", 400)
        
        if not allowed_file(file.filename):
            return error_response("File type not allowed. Only PNG, JPG, JPEG, GIF, WEBP are allowed", 400)
        
        print(f"File received: {file.filename}, Size: {file.content_length} bytes")
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        new_filename = f"guardian_{guardian.guardian_id}_{timestamp}_{unique_id}.{file_extension}"
        
        print(f"Generated filename: {new_filename}")
        
        # Save file with debugging
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        upload_path = os.path.join(upload_folder, 'profile_pics')
        
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, new_filename)
        
        file.save(file_path)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        else:
            return error_response("Failed to save image file", 500)
        
        if guardian.guardian_image_url:
            old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], guardian.guardian_image_url)
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
        
        base_url = request.host_url.rstrip('/')
        image_url = f"{base_url}/uploads/{relative_path}"
        
        return success_response(
            data={
                "image_url": image_url,
                "relative_path": relative_path,
                "avatar": image_url,
                "guardian_image_url": image_url
            },
            message="Profile image uploaded successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        print(f"IMAGE UPLOAD ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return error_response("Failed to upload image", 500, str(e))


@guardian_bp.route("/profile", methods=["GET"])
@guardian_required
def get_my_profile(guardian):
    """Get current logged-in guardian's profile"""
    try:
        guardian_image_url = None
        avatar_url = None
        
        if guardian.guardian_image_url:
            base_url = request.host_url.rstrip('/')
            full_url = f"{base_url}/uploads/{guardian.guardian_image_url}"
            guardian_image_url = full_url
            avatar_url = full_url
        
        guardian_info = {
            "id": guardian.guardian_id,
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name or guardian.username,
            "guardian_name": guardian.guardian_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "cellphone": guardian.contact_number,
            "guardian_image_url": guardian_image_url,  
            "avatar": avatar_url,  
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "village": guardian.village,
            "street_address": guardian.street_address,
            "address": f"{guardian.street_address or ''}, {guardian.barangay or ''}, {guardian.city or ''}, {guardian.province or ''}",
            "role": guardian.role,
            "created_at": (
                guardian.created_at.isoformat() if guardian.created_at else None
            ),
            "updated_at": (
                guardian.updated_at.isoformat() if guardian.updated_at else None
            ),
        }

        return success_response(data=guardian_info)

    except Exception as e:
        print(f"GET PROFILE ERROR: {e}")
        return error_response("Failed to fetch guardian profile", 500, str(e))


@guardian_bp.route("/profile", methods=["PUT"])
@guardian_required
def update_my_profile(guardian):
    """Update current logged-in guardian's profile"""
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

        field_mapping = {
            "fullName": "guardian_name",
            "name": "guardian_name",
            "guardian_name": "guardian_name",
            "email": "email",
            "cellphone": "contact_number",
            "contact_number": "contact_number",
            "avatar": "guardian_image_url",
            "guardian_image_url": "guardian_image_url",
            "province": "province",
            "city": "city",
            "barangay": "barangay",
            "village": "village",
            "street_address": "street_address",
            "address": "street_address",  
        }

        for frontend_field, model_field in field_mapping.items():
            if frontend_field in data:
                if frontend_field == "address" and isinstance(
                    data[frontend_field], str
                ):
                    setattr(guardian, model_field, data[frontend_field])
                elif data[frontend_field] is not None:
                    setattr(guardian, model_field, data[frontend_field])

        if "password" in data and data["password"]:
            guardian.set_password(data["password"])

        db.session.commit()

        guardian_image_url = None
        if guardian.guardian_image_url:
            base_url = request.host_url.rstrip('/')
            guardian_image_url = f"{base_url}/uploads/{guardian.guardian_image_url}"

        updated_info = {
            "id": guardian.guardian_id,
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name or guardian.username,
            "guardian_name": guardian.guardian_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "cellphone": guardian.contact_number,
            "guardian_image_url": guardian_image_url,  # Full URL
            "avatar": guardian_image_url,  # Full URL
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "village": guardian.village,
            "street_address": guardian.street_address,
            "address": f"{guardian.street_address or ''}, {guardian.barangay or ''}, {guardian.city or ''}, {guardian.province or ''}",
            "role": guardian.role,
        }

        return success_response(
            data=updated_info, message="Profile updated successfully"
        )

    except Exception as e:
        db.session.rollback()
        print("UPDATE PROFILE ERROR:", e)
        return error_response("Failed to update profile", 500, str(e))


@guardian_bp.route("/vip-guardians", methods=["GET"])
@guardian_required
def get_vip_guardians(guardian):
    """Get all guardians associated with the same VIPs as current guardian"""
    try:
        vip_guardians = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).all()
        vip_ids = [vg.vip_id for vg in vip_guardians]

        if not vip_ids:
            return success_response(data=[])

        all_vip_guardians = VIPGuardian.query.filter(
            VIPGuardian.vip_id.in_(vip_ids)
        ).all()
        guardian_ids = [vg.guardian_id for vg in all_vip_guardians]

        guardian_ids = [gid for gid in guardian_ids if gid != guardian.guardian_id]

        if not guardian_ids:
            return success_response(data=[])

        guardians = Guardian.query.filter(Guardian.guardian_id.in_(guardian_ids)).all()

        guardian_list = []
        for g in guardians:
            vip_guardian = VIPGuardian.query.filter_by(
                guardian_id=g.guardian_id,
                vip_id=vip_ids[0],  
            ).first()

            guardian_image_url = None
            if g.guardian_image_url:
                base_url = request.host_url.rstrip('/')
                guardian_image_url = f"{base_url}/uploads/{g.guardian_image_url}"

            guardian_info = {
                "id": g.guardian_id,
                "guardian_id": g.guardian_id,
                "username": g.username,
                "name": g.guardian_name or g.username,
                "guardian_name": g.guardian_name,
                "fullName": g.guardian_name,
                "email": g.email,
                "contact_number": g.contact_number,
                "cellphone": g.contact_number,
                "guardian_image_url": guardian_image_url,  # Full URL
                "avatar": guardian_image_url,  # Full URL
                "province": g.province,
                "city": g.city,
                "barangay": g.barangay,
                "village": g.village,
                "street_address": g.street_address,
                "address": f"{g.street_address or ''}, {g.barangay or ''}, {g.city or ''}, {g.province or ''}",
                "relationship": (
                    vip_guardian.relationship_to_vip if vip_guardian else None
                ),
                "created_at": g.created_at.isoformat() if g.created_at else None,
                "updated_at": g.updated_at.isoformat() if g.updated_at else None,
            }
            guardian_list.append(guardian_info)

        return success_response(data=guardian_list)

    except Exception as e:
        return error_response("Failed to fetch VIP guardians", 500, str(e))


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
                base_url = request.host_url.rstrip('/')
                guardian_image_url = f"{base_url}/uploads/{g.guardian_image_url}"

            guardian_list.append(
                {
                    "guardian_id": g.guardian_id,
                    "username": g.username,
                    "guardian_name": g.guardian_name,
                    "email": g.email,
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
            base_url = request.host_url.rstrip('/')
            guardian_image_url = f"{base_url}/uploads/{guardian_data.guardian_image_url}"

        guardian_info = {
            "guardian_id": guardian_data.guardian_id,
            "username": guardian_data.username,
            "guardian_name": guardian_data.guardian_name,
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

        updatable_fields = [
            "guardian_name",
            "email",
            "contact_number",
            "province",
            "city",
            "barangay",
            "village",
            "street_address",
            "guardian_image_url",
        ]

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


@guardian_bp.route("/test", methods=["GET"])
@guardian_required
def test_endpoint(guardian):
    """Test endpoint to verify guardian authentication is working"""
    return success_response(
        message="Guardian endpoint is working",
        data={
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name,
        },
    )