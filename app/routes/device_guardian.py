from flask import Blueprint, request
from app import db
from app.models import DeviceGuardian, Device, Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response

device_guardian_bp = Blueprint('device_guardian', __name__)


@device_guardian_bp.route('', methods=['POST'])
@guardian_required
def assign_guardian(guardian):
    try:
        data = request.get_json() or {}
        device_id = data.get('device_id')
        guardian_id = data.get('guardian_id')
        device_serial = data.get('device_serial_number')

        if not device_id and not device_serial:
            return error_response("`device_id` or `device_serial_number` is required", 400)

        if device_serial and not device_id:
            device = Device.query.filter_by(device_serial_number=device_serial).first()
            if not device:
                return error_response("Device not found", 404)
            device_id = device.device_id

        device = Device.query.get(device_id)
        if not device:
            return error_response("Device not found", 404)

        guardian_obj = Guardian.query.get(guardian_id)
        if not guardian_obj:
            return error_response("Guardian not found", 404)

        existing = DeviceGuardian.query.filter_by(device_id=device_id, guardian_id=guardian_id).first()
        if existing:
            return error_response("Guardian already assigned to this device", 400)

        link = DeviceGuardian(device_id=device_id, guardian_id=guardian_id)
        db.session.add(link)
        db.session.commit()

        return success_response(data={"id": link.id}, message="Guardian assigned to device", status_code=201)

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to assign guardian", 500, str(e))


@device_guardian_bp.route('', methods=['GET'])
@guardian_required
def list_assignments(guardian):
    try:
        device_id = request.args.get('device_id', type=int)
        guardian_id = request.args.get('guardian_id', type=int)

        if device_id:
            links = DeviceGuardian.query.filter_by(device_id=device_id).all()
            data = [
                {
                    "id": l.id,
                    "guardian_id": l.guardian_id,
                    "guardian_name": l.guardian.guardian_name if l.guardian else None,
                    "assigned_at": l.assigned_at.isoformat() if l.assigned_at else None
                }
                for l in links
            ]
            return success_response(data=data)

        if guardian_id:
            links = DeviceGuardian.query.filter_by(guardian_id=guardian_id).all()
            data = [
                {
                    "id": l.id,
                    "device_id": l.device_id,
                    "device_serial_number": l.device.device_serial_number if l.device else None,
                    "assigned_at": l.assigned_at.isoformat() if l.assigned_at else None
                }
                for l in links
            ]
            return success_response(data=data)

        return error_response("Provide `device_id` or `guardian_id` as query parameter", 400)

    except Exception as e:
        return error_response("Failed to fetch assignments", 500, str(e))


@device_guardian_bp.route('/<int:link_id>', methods=['DELETE'])
@guardian_required
def remove_assignment(guardian, link_id):
    try:
        link = DeviceGuardian.query.get(link_id)
        if not link:
            return error_response("Assignment not found", 404)

        db.session.delete(link)
        db.session.commit()

        return success_response(message="Assignment removed successfully")

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to remove assignment", 500, str(e))
