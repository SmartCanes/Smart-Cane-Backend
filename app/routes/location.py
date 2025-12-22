from flask import Blueprint, request
from app import db
from app.models import GPSLocation
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response, paginated_response

location_bp = Blueprint("location", __name__)


@location_bp.route("", methods=["POST"])
@guardian_required
def create_location(guardian):
    try:
        data = request.get_json()

        required_fields = ["vip_id", "latitude", "longitude"]
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)

        location = GPSLocation(
            vip_id=data["vip_id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            location=data.get("location"),
        )

        db.session.add(location)
        db.session.commit()

        return success_response(
            data={"location_id": location.location_id},
            message="Location recorded successfully",
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to record location", 500, str(e))


@location_bp.route("/vip/<int:vip_id>", methods=["GET"])
@guardian_required
def get_vip_locations(guardian, vip_id):
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        locations = (
            GPSLocation.query.filter_by(vip_id=vip_id)
            .order_by(GPSLocation.timestamp.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        location_list = []
        for location in locations.items:
            location_list.append(
                {
                    "location_id": location.location_id,
                    "vip_id": location.vip_id,
                    "latitude": float(location.latitude),
                    "longitude": float(location.longitude),
                    "location": location.location,
                    "timestamp": (
                        location.timestamp.isoformat() if location.timestamp else None
                    ),
                }
            )

        return success_response(
            data=paginated_response(location_list, page, per_page, locations.total)
        )

    except Exception as e:
        return error_response("Failed to fetch locations", 500, str(e))


@location_bp.route("/latest/vip/<int:vip_id>", methods=["GET"])
@guardian_required
def get_latest_location(guardian, vip_id):
    try:
        location = (
            GPSLocation.query.filter_by(vip_id=vip_id)
            .order_by(GPSLocation.timestamp.desc())
            .first()
        )

        if not location:
            return error_response("No location data found", 404)

        location_data = {
            "location_id": location.location_id,
            "vip_id": location.vip_id,
            "latitude": float(location.latitude),
            "longitude": float(location.longitude),
            "location": location.location,
            "timestamp": location.timestamp.isoformat() if location.timestamp else None,
        }

        return success_response(data=location_data)

    except Exception as e:
        return error_response("Failed to fetch latest location", 500, str(e))
