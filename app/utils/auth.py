from functools import wraps
from flask import request
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

def guardian_must_have_device(fn):
    @wraps(fn)
    def wrapper(current_guardian, *args, **kwargs):
        # current_guardian is the Guardian instance injected by jwt_required
        count = DeviceGuardian.query.filter_by(guardian_id=current_guardian.guardian_id).count()
        if count < 1:
            return error_response("No smart cane paired. Scan QR to continue.", 403)
        return fn(current_guardian, *args, **kwargs)
    return wrapper