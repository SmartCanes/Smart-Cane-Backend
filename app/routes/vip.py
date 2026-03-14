from flask import Blueprint, request, current_app
from app import db
from app.models import VIP, DeviceGuardian, Device
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os
import uuid
from app.utils.serializer import model_to_dict
from app.utils.history_logger import log_action

vip_bp = Blueprint("vip", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@vip_bp.route("/<int:vip_id>/image", methods=["POST"])
@guardian_required
def upload_vip_image(guardian, vip_id):
    try:
        device_guardian = (
            DeviceGuardian.query.join(Device)
            .filter(
                DeviceGuardian.guardian_id == guardian.guardian_id,
                Device.vip_id == vip_id,
            )
            .first()
        )

        if not device_guardian:
            return error_response("No access to this VIP", 403)

        vip = VIP.query.get(vip_id)
        if not vip:
            return error_response("VIP not found", 404)

        if "image" not in request.files:
            return error_response("No image file provided", 400)

        file = request.files["image"]
        if file.filename == "":
            return error_response("No selected file", 400)

        if not allowed_file(file.filename):
            return error_response(
                "File type not allowed. Only PNG, JPG, JPEG, GIF, WEBP are allowed", 400
            )

        # Generate unique filename
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit(".", 1)[1].lower()
        new_filename = f"vip_{vip.vip_id}_{timestamp}_{unique_id}.{file_extension}"

        # Upload folder
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        vip_folder = os.path.join(upload_folder, "vip_profiles")
        os.makedirs(vip_folder, exist_ok=True)

        file_path = os.path.join(vip_folder, new_filename)
        file.save(file_path)

        if not os.path.exists(file_path):
            return error_response("Failed to save image file", 500)

        # Delete old image if exists
        if vip.vip_image_url:
            old_image_path = os.path.join(upload_folder, vip.vip_image_url)
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception:
                    pass

        # Save relative path
        relative_path = f"vip_profiles/{new_filename}"
        vip.vip_image_url = relative_path
        vip.updated_at = datetime.now(timezone.utc)

        

        db.session.commit()

        # Build accessible URL
        base_url = request.host_url.rstrip("/")
        image_url = f"{base_url}/uploads/{relative_path}"

        return success_response(
            data={
                "image_url": image_url,
                "relative_path": relative_path,
                "avatar": image_url,
                "vip_image_url": image_url,
            },
            message="VIP profile image uploaded successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to upload VIP image", 500, str(e))


@vip_bp.route("/<int:device_id>", methods=["PUT"])
@guardian_required
def update_vip(guardian, device_id):
    try:
        data = request.get_json() or {}

        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        if device_guardian.role not in ["primary", "secondary"]:
            return error_response(
                "Only primary or secondary guardians can update VIP", 403
            )

        device = Device.query.get(device_id)

        vip = device.vip

        if not vip:
            return error_response("VIP not found", 404)

        vip_data = data.get("vip", {})

        updatable_fields = [
            "first_name",
            "middle_name",
            "last_name",
            "vip_image_url",
            "province",
            "city",
            "barangay",
            "street_address",
        ]

        name_fields = {"first_name", "middle_name", "last_name"}

        for field in updatable_fields:
            if field in vip_data:
                value = vip_data[field]
                if field in name_fields and isinstance(value, str):
                    value = value.title()
                setattr(vip, field, value)

        vip.updated_at = datetime.now(timezone.utc)

        log_action(
            guardian_id=guardian.guardian_id,
            action="UPDATE",
            description=f"{guardian.first_name} {guardian.last_name} updated VIP profile for {vip.first_name} {vip.last_name}",
            device_id=device_id
        )

        db.session.commit()

        response_data = {
            "vip": model_to_dict(vip)
        }

        return success_response(data=response_data, message="VIP updated successfully")

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update VIP", 500, str(e))


@vip_bp.route("/<int:device_id>", methods=["DELETE"])
@guardian_required
def delete_vip(guardian, device_id):
    try:
        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        if device_guardian.role not in ["primary", "secondary"]:
            return error_response(
                "Only primary or secondary guardians can update VIP", 403
            )

        device = Device.query.get(device_id)

        if not device or not device.vip:
            return error_response("VIP not found for this device", 404)

        vip = device.vip

        device.vip_id = None

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        vip_folder = os.path.join(upload_folder, "vip_profiles")
        os.makedirs(vip_folder, exist_ok=True)

        # Delete old image if exists
        if vip.vip_image_url:
            old_image_path = os.path.join(upload_folder, vip.vip_image_url)
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception:
                    pass

        log_action(
            guardian_id=guardian.guardian_id,
            action="DELETE",
            description=f"{guardian.first_name} {guardian.last_name} removed VIP profile for {vip.first_name} {vip.last_name}",
            device_id=device_id
        )

        db.session.delete(vip)
        db.session.commit()

        return success_response(
            message="VIP deleted successfully",
            data={"device_id": device.device_id, "vip_id": vip.vip_id},
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete VIP", 500, str(e))
