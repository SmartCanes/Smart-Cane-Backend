from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import Guardian
from app.utils.responses import error_response

def guardian_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # try:
        #     # verify_jwt_in_request()
        #     # current_user_id = get_jwt_identity()
        #     guardian = Guardian.query.get(current_user_id)
        #     if not guardian:
        #         return error_response("Guardian not found", 404)
        #     return f(guardian, *args, **kwargs)
        # except Exception as e:
        #     return error_response("Invalid token", 401)
            dummy_guardian = None  # or Guardian.query.first()
            return f(dummy_guardian, *args, **kwargs)
    return decorated_function