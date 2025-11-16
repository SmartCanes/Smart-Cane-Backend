from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, details=None):
    response = {
        "success": False,
        "error": status_code,
        "message": message,
        "details": details
    }
    return jsonify(response), status_code

def paginated_response(data, page, per_page, total):
    return {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }