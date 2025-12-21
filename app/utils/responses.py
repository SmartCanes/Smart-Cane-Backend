from flask import jsonify


def snake_to_camel_dict(data: dict) -> dict:
    def snake_to_camel(s):
        parts = s.split("_")
        return parts[0] + "".join(word.capitalize() for word in parts[1:])

    return {snake_to_camel(k): v for k, v in data.items()}


def _camelize(data):
    if data is None:
        return None
    if isinstance(data, dict):
        return snake_to_camel_dict(data)
    if isinstance(data, list):
        return [
            _camelize(item) if isinstance(item, (dict, list)) else item for item in data
        ]
    return data


def success_response(data=None, message="Success", status_code=200):
    response = {"success": True, "message": message, "data": _camelize(data)}
    return jsonify(response), status_code


def error_response(message="Error", status_code=400, details=None):
    response = {
        "success": False,
        "error": status_code,
        "message": message,
        "details": _camelize(details),
    }
    return jsonify(response), status_code


def paginated_response(data, page, per_page, total):
    pagination = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
    }
    return {
        "success": True,
        "data": _camelize(data),
        "pagination": _camelize(pagination),
    }
