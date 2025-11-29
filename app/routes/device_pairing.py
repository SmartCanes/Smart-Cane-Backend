from flask import Blueprint, request
from datetime import datetime, timedelta
import secrets

from app import db
from app.models import Device, DeviceGuardian, Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from app.models import VIP

qr_bp = Blueprint('qr', __name__)


@qr_bp.route('/generate', methods=['POST'])
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
        expires_at = datetime.utcnow() + timedelta(minutes=5)

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
@qr_bp.route('/pair', methods=['POST'])
@guardian_required
def pair_device(guardian: Guardian):
    try:
        data = request.get_json() or {}
        device_serial = data.get('device_serial_number')
        vip_name = data.get('vip_name')
        vip_address = data.get('vip_address')

        if not device_serial:
            return error_response('`device_serial_number` is required', 400)

        device = Device.query.filter_by(device_serial_number=device_serial).first()
        if not device:
            return error_response('Device not found', 404)

        existing_link = DeviceGuardian.query.filter_by(
            device_id=device.device_id,
            guardian_id=guardian.guardian_id
        ).first()
        if existing_link:
            return error_response('Guardian already paired with this device', 400)

        if not device.vip_id:
            if not vip_name:
                return error_response(
                    'VIP information required for first-time pairing', 400
                )
            new_vip = VIP(
                vip_name=vip_name,
                street_address=vip_address,
                created_at=datetime.utcnow()
            )
            db.session.add(new_vip)
            db.session.flush() 
            device.vip_id = new_vip.vip_id

        # 4️⃣ Create link in device_guardian_tbl
        link = DeviceGuardian(device_id=device.device_id, guardian_id=guardian.guardian_id)
        db.session.add(link)

        db.session.commit()

        return success_response(
            data={
                'device_id': device.device_id,
                'device_serial_number': device.device_serial_number,
                'vip_id': device.vip_id,
                'guardian_id': guardian.guardian_id
            },
            message='Device paired successfully',
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response('Failed to pair device', 500, str(e))