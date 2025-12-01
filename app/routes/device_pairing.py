from flask import Blueprint, request
from datetime import datetime, timedelta, timezone
import secrets

from app import db
from app.models import Device, DeviceGuardian, Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from app.models import VIP

device_pairing_bp = Blueprint('device_pairing', __name__)


@device_pairing_bp.route('/generate', methods=['POST'])
@guardian_required
def generate_pairing_token(guardian):
    try:
        data = request.get_json() or {}
        device_id = data.get('device_id')
        device_serial = data.get('device_serial_number')

        if not device_id and not device_serial:
            return error_response('Provide `device_id` or `device_serial_number`', 400)

        if device_serial and not device_id:
            device = Device.query.filter_by(device_serial_number=device_serial).first()
            if not device:
                return error_response('Device not found', 404)
            device_id = device.device_id

        device = Device.query.get(device_id)
        if not device:
            return error_response('Device not found', 404)

        token = secrets.token_urlsafe(24)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        device.pairing_token = token
        device.pairing_token_expires_at = expires_at
        db.session.commit()

        return success_response(data={
            'pairing_token': token,
            'expires_at': expires_at.isoformat()
        }, message='Pairing token generated', status_code=201)

    except Exception as e:
        db.session.rollback()
        return error_response('Failed to generate pairing token', 500, str(e))
    
@device_pairing_bp.route('/validate', methods=['GET'])
def validate_device_serial():
    serial = request.args.get('device_serial')

    if not serial:
        return error_response("device_serial is required", 400)

    device = Device.query.filter_by(device_serial_number=serial).first()

    if not device:
        return success_response(
            data={"valid": False, "reason": "not_found"},
            message="Device serial is invalid"
        )

    if device.vip_id is not None:
        return success_response(
            data={"valid": False, "reason": "already_paired"},
            message="Device is already paired to another guardian"
        )

    return success_response(
        data={"valid": True, "reason": "ok", "device_serial_number": serial},
        message="Device serial is available"
    )

@device_pairing_bp.route('/pair', methods=['POST'])
def pair_device():
    try:
        data = request.get_json() or {}
        device_serial = data.get('device_serial_number')
        guardian_id = data.get('guardian_id')

        if not device_serial:
            return error_response('`device_serial_number` is required', 400)

        device = Device.query.filter_by(device_serial_number=device_serial).first()
        if not device:
            return error_response('Device not found', 404)

        if device.is_paired:
            return error_response('Device already paired', 400)
        
        if not guardian_id:
            return error_response('`guardian_id` is required to pair device', 400)

        device.is_paired = True  
        device.paired_at = datetime.now(timezone.utc)

        device_guardian = DeviceGuardian(
            device_id=device.device_id,
            guardian_id=guardian_id
        )

        db.session.add(device_guardian)
        db.session.commit()

        return success_response(
            data={
                'device_id': device.device_id,
                'device_serial_number': device.device_serial_number,
                'vip_id': device.vip_id
            },
            message='Device paired successfully!',
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_response('Failed to pair device', 500, str(e))

