import os
from flask import Blueprint, current_app, request
from datetime import datetime, timedelta, timezone
import secrets

from flask_jwt_extended import jwt_required
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import func

from app import db
from app.models import Device, DeviceGuardian, Guardian, GuardianInvitation
from app.routes import guardian
from app.utils.auth import guardian_required
from app.utils.email_service import send_guardian_invite_email
from app.utils.responses import success_response, error_response
from app.models import VIP
from app.utils.serializer import model_to_dict
from app.utils.history_logger import log_action

device = Blueprint("device", __name__)


INVITE_TOKEN_SALT = "guardian-invite"
INVITE_TOKEN_MAX_AGE = 60 * 60 * 24


def generate_guardian_invite_token(payload: dict) -> str:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(payload, salt=INVITE_TOKEN_SALT)


def verify_guardian_invite_token(token: str) -> dict:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.loads(
        token,
        salt=INVITE_TOKEN_SALT,
        max_age=INVITE_TOKEN_MAX_AGE,
    )


@device.route("/decode-invite/<token>", methods=["GET"])
def decode_guardian_invite(token):

    try:
        try:
            payload = verify_guardian_invite_token(token)
        except SignatureExpired:
            return error_response("Invite link has expired", 410)
        except BadSignature:
            return error_response("Invalid invite link", 400)

        return success_response(
            data=payload,
            message="Invite token decoded successfully",
        )

    except Exception as e:
        return error_response("Failed to decode invite token", 500, str(e))


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
            device_id=device.device_id,
            guardian_id=guardian_id,
            role="primary",
            is_emergency_contact=True,
        )

        log_action(
            guardian_id=guardian_id,
            action="PAIR",
            description=f"{guardian.first_name} {guardian.last_name} paired device {device_serial}",
            device_id=device.device_id 
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

        db.session.delete(device_guardian)
        db.session.flush()

        primary_guardians_left = DeviceGuardian.query.filter_by(
            device_id=device_id, role="primary"
        ).count()

        if primary_guardians_left == 0:
            DeviceGuardian.query.filter_by(device_id=device_id).delete()
            device.is_paired = False
            device.paired_at = None
        else:
            device.is_paired = True

        log_action(
            guardian_id=guardian.guardian_id,
            action="UNPAIR",
            description=f"{guardian.first_name} {guardian.last_name} unpaired device ID {device_id}",
            device_id=device_id 
        )
       

        db.session.commit()

        remaining_guardians = DeviceGuardian.query.filter_by(
            device_id=device_id
        ).count()

        return success_response(
            message="Device unpaired successfully",
            data={
                "device_id": device.device_id,
                "vip_id": vip_id,
                "unpaired_guardian_id": guardian.guardian_id,
                "remaining_guardians": remaining_guardians,
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

        if device_guardian.role not in ["primary", "secondary"]:
            return error_response(
                "Only primary or secondary guardians can add VIP profile", 403
            )

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

        log_action(
            guardian_id=guardian.guardian_id,
            action="CREATE",
            description=f"{guardian.first_name} {guardian.last_name} created VIP profile for {new_vip.first_name} {new_vip.last_name}",
            device_id=device_id             
        )

        db.session.add(new_vip)
        db.session.flush() 

        device.vip_id = new_vip.vip_id

        log_action(
            guardian_id=guardian.guardian_id,
            action="CREATE",
            description=f"{guardian.first_name} {guardian.last_name} created VIP profile for {new_vip.first_name} {new_vip.last_name}"
        )
        db.session.commit()

        response_data = {
            "device_id": device.device_id,
            "device_serial_number": device.device_serial_number,
            "vip": model_to_dict(new_vip),
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
        email = data.get("email")

        if not email:
            return error_response("Email is required", 400)

        if email == guardian.email:
            return error_response("You cannot invite yourself", 400)

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        device_guardian_link = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian.guardian_id
        ).first()

        if not device_guardian_link:
            return error_response("You are not linked to this device", 403)

        if device_guardian_link.role not in ["primary", "secondary"]:
            return error_response(
                "Only primary or secondary guardians can invite new guardians", 403
            )

        guardian_existing = (
            Guardian.query.filter_by(email=email).first() if email else None
        )

        if guardian_existing:
            device_guardian = DeviceGuardian.query.filter_by(
                device_id=device_id, guardian_id=guardian_existing.guardian_id
            ).first()
            if device_guardian:
                return error_response("The user is already linked to this device", 400)

        existing_invite = GuardianInvitation.query.filter_by(
            email=email,
            device_id=device_id,
            status="pending",
        ).first()

        if existing_invite:
            return error_response("An invitation is already pending", 409)

        vip = VIP.query.get(device.vip_id) if device.vip_id else None
        vip_name = f"{vip.first_name} {vip.last_name}" if vip else None

        token = generate_guardian_invite_token(
            {
                "email": email,
                "device_id": device_id,
                "invited_by_guardian_id": guardian.guardian_id,
            }
        )
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        invitation = GuardianInvitation(
            token=token,
            email=email,
            device_id=device_id,
            invited_by_guardian_id=guardian.guardian_id,
            expires_at=expires_at,
        )

        db.session.add(invitation)

        log_action(
            guardian_id=guardian.guardian_id,
            action="INVITE",
            description=f"{guardian.first_name} {guardian.last_name} invited {email} to monitor a device",
            device_id=device_id
        )
        
        db.session.commit()

        FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
        invite_link = f"{FRONTEND_URL}/guardian-invite/{token}"

        email_sent = send_guardian_invite_email(
            recipient_email=email,
            invite_link=invite_link,
            guardian_name=guardian.first_name,
            vip_name=vip_name,
            sender_name=f"{guardian.first_name} {guardian.last_name}",
        )

        if not email_sent:
            return error_response("Failed to send invite email", 500)

        return success_response(
            data={"email": email},
            message="Guardian invite sent successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to send guardian invite", 500, str(e))


from flask_jwt_extended import get_jwt_identity


@device.route("/accept-invite/<token>", methods=["GET"])
@jwt_required(optional=True)
def accept_guardian_invite(token):
    try:
        try:
            payload = verify_guardian_invite_token(token)
        except SignatureExpired:
            return error_response("Invite link has expired", 410)
        except BadSignature:
            return error_response("Invalid invite link", 400)

        current_guardian_id = int(get_jwt_identity()) if get_jwt_identity() else None

        invitation = GuardianInvitation.query.filter_by(
            token=token,
            status="pending",
        ).first()

        if not invitation:
            return error_response("Invalid or expired invite link", 400)

        if (
            current_guardian_id
            and current_guardian_id == invitation.invited_by_guardian_id
        ):
            return error_response("You cannot accept your own invitation.", 403)

        if datetime.now(timezone.utc) > invitation.expires_at.replace(
            tzinfo=timezone.utc
        ):
            invitation.status = "expired"
            db.session.commit()
            return error_response("Invite link has expired", 410)

        if (
            payload["email"] != invitation.email
            or payload["device_id"] != invitation.device_id
        ):
            return error_response("Invalid invite link", 400)

        existing_guardian = Guardian.query.filter_by(email=invitation.email).first()

        # User is logged in
        if current_guardian_id:
            if (
                existing_guardian
                and existing_guardian.guardian_id != current_guardian_id
            ):
                return error_response(
                    "This invitation is for a different guardian account.",
                    403,
                )

            guardian_to_link = existing_guardian or Guardian.query.get(
                current_guardian_id
            )

            existing_link = DeviceGuardian.query.filter_by(
                guardian_id=guardian_to_link.guardian_id,
                device_id=invitation.device_id,
            ).first()

            if existing_link:
                return error_response("You are already linked to this device.", 400)

            db.session.add(
                DeviceGuardian(
                    guardian_id=guardian_to_link.guardian_id,
                    device_id=invitation.device_id,
                    assigned_at=datetime.now(timezone.utc),
                )
            )

            invitation.status = "accepted"
            invitation.accepted_at = datetime.now(timezone.utc)

            log_action(
                guardian_id=guardian_to_link.guardian_id,
                action="ACCEPT_INVITE",
                description=f"{guardian_to_link.first_name} {guardian_to_link.last_name} accepted the invitation to monitor device {invitation.device_id}",
                device_id=invitation.device_id
            )
            db.session.commit()

            return success_response(
                data={
                    "user_exists": True,
                    "guardian_id": guardian_to_link.guardian_id,
                    "redirect_to": "dashboard",
                    "email": invitation.email,
                },
                message="Invitation accepted and device linked.",
            )

        # User not logged in but account exists
        if existing_guardian:
            existing_link = DeviceGuardian.query.filter_by(
                guardian_id=existing_guardian.guardian_id,
                device_id=invitation.device_id,
            ).first()

            if existing_link:
                return error_response("You are already linked to this device.", 400)

            db.session.add(
                DeviceGuardian(
                    guardian_id=existing_guardian.guardian_id,
                    device_id=invitation.device_id,
                    assigned_at=datetime.now(timezone.utc),
                )
            )

            invitation.status = "accepted"
            invitation.accepted_at = datetime.now(timezone.utc)

            log_action(
                guardian_id=existing_guardian.guardian_id,
                action="ACCEPT_INVITE",
                description=f"{existing_guardian.first_name} {existing_guardian.last_name} accepted the invitation to monitor device {invitation.device_id}",
                device_id=invitation.device_id
            )
            db.session.commit()

            return success_response(
                data={
                    "user_exists": True,
                    "guardian_id": existing_guardian.guardian_id,
                    "redirect_to": "login",
                    "email": invitation.email,
                },
                message="Invitation accepted. Please log in.",
            )

        return success_response(
            data={
                "user_exists": False,
                "redirect_to": "register",
            },
            message="Please register to accept the invitation.",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to process invitation", 500, str(e))


@device.route("/<int:device_id>/guardians", methods=["GET"])
@guardian_required
def get_device_guardians(guardian, device_id):
    try:
        if not device_id:
            return error_response("device_id is required", 400)

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        requester_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=guardian.guardian_id,
        ).first()

        if not requester_link:
            return error_response(
                "You are not authorized to view guardians for this device", 403
            )

        device_guardians = (
            db.session.query(DeviceGuardian, Guardian)
            .join(Guardian, Guardian.guardian_id == DeviceGuardian.guardian_id)
            .filter(DeviceGuardian.device_id == device_id)
            .all()
        )

        guardians = []
        for dg, g in device_guardians:
            guardians.append(
                {
                    "guardian_id": g.guardian_id,
                    "username": g.username,
                    "first_name": g.first_name,
                    "middle_name": g.middle_name,
                    "last_name": g.last_name,
                    "email": g.email,
                    "contact_number": g.contact_number,
                    "role": g.role,
                    "relationship": dg.relationship,
                    "street_address": g.street_address,
                    "is_emergency_contact": bool(dg.is_emergency_contact),
                    "assigned_at": (
                        dg.assigned_at.isoformat() if dg.assigned_at else None
                    ),
                }
            )

        return success_response(
            data={"guardians": guardians},
            message="Guardians associated with device retrieved successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to retrieve guardians for device", 500, str(e))


@device.route("/guardians", methods=["GET"])
@guardian_required
def get_all_device_guardians(guardian):
    try:
        device_links = DeviceGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).all()
        device_ids = [dl.device_id for dl in device_links]

        if not device_ids:
            return success_response(
                data={"guardiansByDevice": []},
                message="No devices found for this guardian",
            )

        all_device_guardians = (
            db.session.query(DeviceGuardian, Guardian)
            .join(Guardian, Guardian.guardian_id == DeviceGuardian.guardian_id)
            .filter(DeviceGuardian.device_id.in_(device_ids))
            .all()
        )

        guardians_by_device = {}
        for dg, g in all_device_guardians:
            device_id = dg.device_id
            if device_id not in guardians_by_device:
                guardians_by_device[device_id] = []

            guardians_by_device[device_id].append(
                {
                    "guardian_id": g.guardian_id,
                    "username": g.username,
                    "first_name": g.first_name,
                    "middle_name": g.middle_name,
                    "last_name": g.last_name,
                    "email": g.email,
                    "contact_number": g.contact_number,
                    "role": dg.role,
                    "relationship": dg.relationship,
                    "street_address": g.street_address,
                    "is_emergency_contact": bool(dg.is_emergency_contact),
                    "guardian_image_url": g.guardian_image_url,
                    "assigned_at": (
                        dg.assigned_at.isoformat() if dg.assigned_at else None
                    ),
                }
            )

        for device_id, guardians in guardians_by_device.items():
            guardians.sort(
                key=lambda g: 0 if g["guardian_id"] == guardian.guardian_id else 1
            )

        guardians_by_device_list = [
            {"deviceId": device_id, "guardians": guardians}
            for device_id, guardians in guardians_by_device.items()
        ]

        return success_response(
            data={"guardiansByDevice": guardians_by_device_list},
            message="All device guardians retrieved successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            "Failed to retrieve guardians for all devices", 500, str(e)
        )


@device.route("/<int:device_id>/guardians/<int:guardian_id>", methods=["DELETE"])
@guardian_required
def remove_guardian_from_device(current_guardian, device_id, guardian_id):
    try:
        if current_guardian.guardian_id == guardian_id:
            return error_response(
                "You cannot remove yourself from the device",
                403,
            )

        requester_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=current_guardian.guardian_id,
        ).first()

        if not requester_link:
            return error_response(
                "You are not authorized to manage guardians for this device",
                403,
            )

        if requester_link.role == "guardian":
            return error_response(
                "Guardians with role 'guardian' cannot remove other guardians", 403
            )

        target_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=guardian_id,
        ).first()

        if not target_link:
            return error_response(
                "Guardian is not linked to this device",
                404,
            )

        if target_link.role == "primary":
            return error_response("Primary guardians cannot be removed by anyone", 403)
        if requester_link.role == "secondary" and target_link.role == "secondary":
            return error_response(
                "Secondary guardians cannot remove other secondary guardians", 403
            )

        db.session.delete(target_link)

        log_action(
            guardian_id=current_guardian.guardian_id,
            action="REMOVE_GUARDIAN",
            description=f"{current_guardian.first_name} {current_guardian.last_name} removed guardian ID {guardian_id} from device {device_id}",
            device_id=device_id
        )
       
        db.session.commit()

        return success_response(
            message="Guardian removed from device successfully",
            data={
                "device_id": device_id,
                "removed_guardian_id": guardian_id,
                "requested_by": current_guardian.guardian_id,
            },
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            "Failed to remove guardian from device",
            500,
            str(e),
        )


@device.route("/<int:device_id>/guardians/<int:guardian_id>/role", methods=["PUT"])
@guardian_required
def modify_device_guardian_role(current_guardian, device_id, guardian_id):
    try:
        data = request.get_json() or {}
        new_role = data.get("role")

        if new_role not in ["secondary", "guardian"]:
            return error_response(
                "Invalid role. Must be 'secondary', or 'guardian'.", 400
            )

        requester_link = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=current_guardian.guardian_id
        ).first()
        if not requester_link:
            return error_response(
                "You are not authorized to modify guardians for this device", 403
            )

        if requester_link.role not in ["primary", "secondary", "guardian"]:
            return error_response(
                "Only primary or secondary guardians can modify roles", 403
            )

        target_link = DeviceGuardian.query.filter_by(
            device_id=device_id, guardian_id=guardian_id
        ).first()
        if not target_link:
            return error_response("Target guardian not found for this device", 404)

        if requester_link.role == "secondary" and target_link.role == "primary":
            return error_response(
                "Secondary guardian cannot modify the primary guardian", 403
            )

        target_link.role = new_role

        log_action(
            guardian_id=current_guardian.guardian_id,
            action="UPDATE_ROLE",
            description=f"{current_guardian.first_name} {current_guardian.last_name} changed guardian ID {guardian_id}'s role to {new_role} on device {device_id}",
            device_id=device_id
        )
       
        db.session.commit()

        return success_response(
            data={
                "device_id": device_id,
                "guardian_id": guardian_id,
                "new_role": new_role,
                "modified_by": current_guardian.guardian_id,
            },
            message="Guardian role updated successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update guardian role", 500, str(e))


@device.route(
    "/<int:device_id>/guardians/<int:guardian_id>/relationship", methods=["PUT"]
)
@guardian_required
def update_guardian_relationship(guardian, device_id, guardian_id):
    try:
        data = request.get_json() or {}
        new_relationship = data.get("relationship")

        if not new_relationship:
            return error_response("relationship is required", 400)

        requester_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=guardian.guardian_id,
        ).first()

        if not requester_link:
            return error_response(
                "You are not authorized to modify guardians for this device",
                403,
            )

        target_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=guardian_id,
        ).first()

        if not target_link:
            return error_response("Guardian not linked to this device", 404)

        if requester_link.role == "guardian":
            return error_response(
                "Guardians cannot modify any relationships",
                403,
            )

        if requester_link.role == "secondary":
            if (
                target_link.role in ["primary", "secondary"]
                and guardian.guardian_id != guardian_id
            ):
                return error_response(
                    "Secondary guardians cannot modify primary or other secondary guardians",
                    403,
                )

        target_link.relationship = new_relationship.strip()
        db.session.commit()

        return success_response(
            data={
                "device_id": device_id,
                "guardian_id": guardian_id,
                "relationship": target_link.relationship,
                "updated_by": guardian.guardian_id,
            },
            message="Guardian relationship updated successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            "Failed to update guardian relationship",
            500,
            str(e),
        )


@device.route("/<int:device_id>/guardians/<int:guardian_id>/emergency", methods=["PUT"])
@guardian_required
def toggle_emergency_guardian(current_guardian, device_id, guardian_id):
    try:
        requester_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=current_guardian.guardian_id,
        ).first()

        if not requester_link:
            return error_response(
                "You are not authorized to modify guardians for this device",
                403,
            )

        target_link = DeviceGuardian.query.filter_by(
            device_id=device_id,
            guardian_id=guardian_id,
        ).first()

        if not target_link:
            return error_response("Guardian not linked to this device", 404)

        if requester_link.role != "primary":
            return error_response(
                "Only primary guardians can modify emergency settings",
                403,
            )

        if target_link.is_emergency_contact:
            target_link.is_emergency_contact = False
            db.session.commit()

            return success_response(
                data={
                    "device_id": device_id,
                    "guardian_id": guardian_id,
                    "is_emergency_contact": False,
                    "role": target_link.role,
                },
                message="Emergency guardian removed successfully",
            )

        DeviceGuardian.query.filter_by(
            device_id=device_id,
            is_emergency_contact=True,
        ).update({"is_emergency_contact": False})

        target_link.is_emergency_contact = True
        db.session.commit()

        return success_response(
            data={
                "device_id": device_id,
                "guardian_id": guardian_id,
                "is_emergency_contact": True,
                "role": target_link.role,
            },
            message="Emergency guardian set successfully",
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            "Failed to update emergency guardian",
            500,
            str(e),
        )

@device.route("/pending-invites", methods=["GET"])
@guardian_required
def get_pending_invites_counts(guardian):
    try:
        linked_devices = DeviceGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).all()
        device_ids = [link.device_id for link in linked_devices]

        if not device_ids:
            return success_response(
                data={"pending_invites_counts": []},
                message="No devices linked to this guardian"
            )

        pending_counts = (
            db.session.query(
                GuardianInvitation.device_id,
                func.count(GuardianInvitation.id).label("pending_count")
            )
            .filter(
                GuardianInvitation.device_id.in_(device_ids),
                GuardianInvitation.status == "pending"
            )
            .group_by(GuardianInvitation.device_id)
            .all()
        )

        result = [
            {"device_id": device_id, "pending_invites_count": count}
            for device_id, count in pending_counts
        ]

        for device_id in device_ids:
            if device_id not in [r["device_id"] for r in result]:
                result.append({"device_id": device_id, "pending_invites_count": 0})

        return success_response(
            data={"pending_invites_counts": result},
            message="Pending invites count per device retrieved successfully"
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            "Failed to retrieve pending invites counts",
            500,
            str(e)
        )