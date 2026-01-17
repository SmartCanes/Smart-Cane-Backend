import os
from flask import Blueprint, request
from datetime import datetime, timedelta, timezone
import secrets

from app import db
from app.models import OTP, Device, DeviceGuardian, Guardian
from app.routes.auth import check_otp_rate_limit
from app.utils.auth import guardian_required
from app.utils.email_service import send_guardian_invite_email
from app.utils.responses import success_response, error_response
from app.models import VIP
from app.utils.serializer import model_to_dict

device = Blueprint("device", __name__)


@device.route("/generate", methods=["POST"])
@guardian_required
def generate_pairing_token(guardian):
    try:
        data = request.get_json() or {}
        device_id = data.get("device_id")
        device_serial = data.get("device_serial_number")

        if not device_id and not device_serial:
            return error_response("Provide `device_id` or `device_serial_number`", 400)

        if device_serial and not device_id:
            device = Device.query.filter_by(device_serial_number=device_serial).first()
            if not device:
                return error_response("Device not found", 404)
            device_id = device.device_id

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        token = secrets.token_urlsafe(24)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        device.pairing_token = token
        device.pairing_token_expires_at = expires_at
        db.session.commit()

        return success_response(
            data={"pairing_token": token, "expires_at": expires_at.isoformat()},
            message="Pairing token generated",
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to generate pairing token", 500, str(e))


@device.route("/validate", methods=["GET"])
def validate_device_serial():
    serial = request.args.get("device_serial")

    if not serial:
        return error_response("device_serial is required", 400)

    device = Device.query.filter_by(device_serial_number=serial).first()
    if not device:
        return success_response(
            data={"valid": False, "reason": "not_found"},
            message="Device serial is invalid",
        )

    if device.is_paired:
        return success_response(
            data={"valid": False, "reason": "already_paired"},
            message="Device is already paired to another guardian",
        )

    return success_response(
        data={"valid": True, "reason": "ok", "device_serial_number": serial},
        message="Device serial is available",
    )


@device.route("/pair", methods=["POST"])
@guardian_required
def pair_device(guardian):
    try:
        data = request.get_json() or {}
        device_serial = data.get("device_serial_number")
        guardian_id = guardian.guardian_id

        if not device_serial:
            return error_response("`device_serial_number` is required", 400)

        device = Device.query.filter_by(device_serial_number=device_serial).first()
        if not device:
            return error_response("Device not found", 404)

        if device.is_paired:
            return error_response("Device already paired", 400)

        if not guardian_id:
            return error_response("`guardian_id` is required to pair device", 400)

        device.is_paired = True
        device.paired_at = datetime.now(timezone.utc)

        device_guardian = DeviceGuardian(
            device_id=device.device_id, guardian_id=guardian_id
        )

        db.session.add(device_guardian)
        db.session.commit()

        return success_response(
            data=model_to_dict(
                device, exclude_fields=["is_paired", "created_at", "updated_at"]
            ),
            message="Device paired successfully!",
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_response("Failed to pair device", 500, str(e))


@device.route("/unpair/<int:device_id>", methods=["POST"])
@guardian_required
def unpair_device(guardian, device_id):
    try:
        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        vip_id = None
        if device.vip:
            vip_id = device.vip.vip_id
            db.session.delete(device.vip)

        device.vip_id = None
        device.is_paired = False
        device.paired_at = None

        db.session.delete(device_guardian)

        db.session.commit()

        return success_response(
            message="Device unpaired successfully",
            data={
                "device_id": device.device_id,
                "vip_id": vip_id,
                "guardian_id": guardian.guardian_id,
            },
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to unpair device", 500, str(e))


@device.route("/list", methods=["GET"])
@guardian_required
def get_devices(guardian):
    try:
        guardian_id = guardian.guardian_id

        device_guardians = DeviceGuardian.query.filter_by(guardian_id=guardian_id).all()
        devices = []
        for dg in device_guardians:
            device = Device.query.get(dg.device_id)
            if device:
                vip = VIP.query.get(device.vip_id)
                devices.append(
                    {
                        "device_id": device.device_id,
                        "device_name": dg.device_name,
                        "device_serial_number": device.device_serial_number,
                        "last_active_at": (
                            device.last_active_at.isoformat()
                            if device.last_active_at
                            else None
                        ),
                        "relationship": dg.relationship,
                        "is_emergency_contact": dg.is_emergency_contact,
                        "vip": (model_to_dict(vip) if vip else None),
                        "paired_at": (
                            device.paired_at.isoformat() if device.paired_at else None
                        ),
                    }
                )

        return success_response(
            data={"devices": devices},
            message="Devices retrieved successfully",
        )

    except Exception as e:
        print(e)
        return error_response("Failed to retrieve devices", 500, str(e))


@device.route("/vip/<int:device_id>", methods=["POST"])
@guardian_required
def assign_device_to_vip(guardian, device_id):
    try:
        data = request.get_json() or {}

        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        device = Device.query.get(device_id)

        if device.vip_id:
            return error_response("Device is already assigned to a VIP", 400)

        vip_data = data.get("vip")
        if not vip_data:
            return error_response("VIP data is required", 400)

        required_fields = ["first_name", "last_name", "province", "city", "barangay"]
        for field in required_fields:
            if not vip_data.get(field):
                return error_response(f"Missing required VIP field: {field}", 400)

        new_vip = VIP(
            first_name=vip_data.get("first_name"),
            middle_name=vip_data.get("middle_name"),
            last_name=vip_data.get("last_name"),
            vip_image_url=vip_data.get("vip_image_url", ""),
            province=vip_data.get("province"),
            city=vip_data.get("city"),
            barangay=vip_data.get("barangay"),
            street_address=vip_data.get("street_address", ""),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        db.session.add(new_vip)
        db.session.flush()  # get vip_id

        device.vip_id = new_vip.vip_id

        device_guardian.relationship = data.get("relationship")
        device_guardian.is_emergency_contact = bool(data.get("is_emergency_contact"))

        db.session.commit()

        response_data = {
            "device_id": device.device_id,
            "device_serial_number": device.device_serial_number,
            "vip": model_to_dict(new_vip),
            "relationship": device_guardian.relationship,
            "is_emergency_contact": bool(device_guardian.is_emergency_contact),
            "paired_at": device.paired_at,
            "guardian_id": guardian.guardian_id,
        }

        return success_response(
            data=response_data, message="Device assigned to VIP successfully"
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to assign device to VIP", 500, str(e))


@device.route("/<int:device_id>/name", methods=["PUT"])
@guardian_required
def update_device_name(guardian, device_id):
    try:
        data = request.get_json() or {}

        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        new_name = data.get("device_name")

        device_guardian.device_name = new_name
        db.session.commit()

        return success_response(
            data={
                "device_id": device_id,
                "device_name": new_name,
            },
            message="Device name updated successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update device name", 500, str(e))


@device.route("/<int:device_id>/last_active_at", methods=["POST"])
@guardian_required
def update_device_active_status(guardian, device_id):
    try:
        data = request.get_json() or {}

        if not device_id:
            return error_response("device_id is required", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Device not paired with this guardian", 404)

        last_active_at = data.get("last_active_at")

        if last_active_at is None:
            return error_response("last_active_at is required", 400)

        device_guardian.active_status = last_active_at
        db.session.commit()

        return success_response(
            data={
                "device_id": device_id,
                "last_active_at": last_active_at,
            },
            message="Device active status updated successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update device active status", 500, str(e))


@device.route("/<int:device_id>/invite-guardian", methods=["POST"])
@guardian_required
def invite_guardian_to_device_link(guardian, device_id):
    try:
        data = request.get_json() or {}
        email = data.get("email", "")

        if not email:
            return error_response("Email is required", 400)

        if email == guardian.email:
            return error_response("Cannot invite yourself as guardian", 400)

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        if not check_otp_rate_limit(email, "vip_guardian_invite"):
            return error_response(
                "Too many invite attempts. Please try again later.", 429
            )

        vip = VIP.query.get(device.vip_id) if device.vip_id else None
        vip_name = f"{vip.first_name} {vip.last_name}" if vip else None

        token = secrets.token_urlsafe(24)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        otp_record = OTP(
            email=email,
            otp_code=token,
            expires_at=expires_at,
            is_used=False,
            purpose="vip_guardian_invite_link",
        )

        db.session.add(otp_record)
        db.session.commit()

        FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
        invite_link = f"{FRONTEND_URL}/guardian-invite?token={token}"

        print(guardian.first_name)
        email_sent = send_guardian_invite_email(
            recipient_email=email,
            invite_link=invite_link,
            guardian_name=guardian.first_name,
            vip_name=vip_name,
            sender_name=guardian.first_name + " " + guardian.last_name,
        )

        if not email_sent:
            return error_response("Failed to send invite email", 500)

        return success_response(
            data={"email": email} or {},
            message="Guardian invite sent successfully via link",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to send guardian invite", 500, str(e))


@device.route("/vip/accept-invite", methods=["POST"])
@guardian_required
def accept_guardian_invite_link(guardian):
    try:
        data = request.get_json()
        token = data.get("token")

        if not token:
            return error_response("Invite token is required", 400)

        otp = OTP.query.filter_by(
            otp_code=token, is_used=False, purpose="vip_guardian_invite_link"
        ).first()

        if not otp:
            return error_response("Invalid or expired invite link", 400)

        if datetime.now(timezone.utc) > otp.expires_at.replace(tzinfo=timezone.utc):
            return error_response("Invite link has expired", 400)

        device_guardian = DeviceGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian:
            return error_response("Guardian has no registered device", 404)

        device = Device.query.get(device_guardian.device_id)
        device.vip_id = Device.query.get(device_guardian.device_id).vip_id or otp.vip_id

        otp.is_used = True
        otp.used_at = datetime.now(timezone.utc)

        db.session.commit()

        return success_response(
            data={"guardian_id": device_guardian.guardian_id},
            message="Guardian successfully assigned to VIP via invite link",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to accept guardian invite", 500, str(e))
