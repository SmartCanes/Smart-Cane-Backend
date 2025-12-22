from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import Guardian, DeviceGuardian
from app.utils.responses import error_response


def guardian_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()

            current_guardian_id = get_jwt_identity()
            guardian = Guardian.query.get(current_guardian_id)

            if not guardian:
                return error_response("Guardian not found", 404)

            # Pass the guardian instance to the endpoint
            return f(guardian, *args, **kwargs)

        except Exception as e:
            return error_response("Invalid or expired token", 401, str(e))

    return decorated_function


def guardian_with_device_required(f):
    @wraps(f)
    def decorated_function(guardian, *args, **kwargs):
        devices = DeviceGuardian.query.filter_by(guardian_id=guardian.guardian_id).all()
        if not devices:
            return jsonify({"success": False, "message": "No devices paired."}), 403
        kwargs["devices"] = devices
        return f(guardian, *args, **kwargs)

    return decorated_function
