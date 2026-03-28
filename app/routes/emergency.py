from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from .. import db                     # relative import from parent package
from ..models import DeviceLog

emergency_bp = Blueprint("emergency", __name__)


def require_admin():
    claims = get_jwt()
    if claims.get("role") not in ("super_admin", "admin"):
        return jsonify({"message": "Access denied."}), 403
    return None


@emergency_bp.route("/", methods=["GET"])
@jwt_required()
def list_emergency_logs():
    """Return logs with activity_type in emergency categories."""
    err = require_admin()
    if err:
        return err

    # Types considered as emergencies
    emergency_types = ["sos_triggered", "device_down", "emergency_alert", "fall_detected"]

    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)

    logs = (
        DeviceLog.query
        .filter(DeviceLog.activity_type.in_(emergency_types))
        .order_by(DeviceLog.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    result = []
    for log in logs:
        device = log.device
        if not device:
            continue

        vip = device.vip
        guardians = []
        for link in device.guardian_links:
            g = link.guardian
            guardians.append({
                "guardian_id": g.guardian_id,
                "first_name": g.first_name,
                "last_name": g.last_name,
                "email": g.email,
                "role": link.role,
            })

        result.append({
            "id": log.log_id,
            "device_serial_number": device.device_serial_number,
            "vip": {
                "vip_id": vip.vip_id,
                "first_name": vip.first_name,
                "last_name": vip.last_name,
            } if vip else None,
            "guardians": guardians,
            "log_message": log.message,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        })

    return jsonify(result), 200