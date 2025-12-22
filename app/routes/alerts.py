from flask import Blueprint, request
from app import db
from app.models import EmergencyAlert, GPSLocation
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response, paginated_response

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("", methods=["POST"])
@guardian_required
def create_alert(guardian):
    try:
        data = request.get_json()

        required_fields = ["vip_id", "latitude", "longitude"]
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)

        # First create location record
        location = GPSLocation(
            vip_id=data["vip_id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            location=data.get("location"),
        )
        db.session.add(location)
        db.session.flush()  # Get the location_id without committing

        # Then create alert record
        alert = EmergencyAlert(vip_id=data["vip_id"], location_id=location.location_id)
        db.session.add(alert)
        db.session.commit()

        return success_response(
            data={"alert_id": alert.alert_id},
            message="Emergency alert created successfully",
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create emergency alert", 500, str(e))


@alerts_bp.route("", methods=["GET"])
@guardian_required
def get_alerts(guardian):
    try:
        vip_id = request.args.get("vip_id", type=int)
        acknowledged = request.args.get("acknowledged", type=int)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        query = EmergencyAlert.query.join(GPSLocation)

        if vip_id:
            query = query.filter(EmergencyAlert.vip_id == vip_id)

        if acknowledged is not None:
            query = query.filter(EmergencyAlert.acknowledged == bool(acknowledged))

        alerts = query.order_by(EmergencyAlert.triggered_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        alert_list = []
        for alert in alerts.items:
            alert_list.append(
                {
                    "alert_id": alert.alert_id,
                    "vip_id": alert.vip_id,
                    "location_id": alert.location_id,
                    "latitude": float(alert.location.latitude),
                    "longitude": float(alert.location.longitude),
                    "location": alert.location.location,
                    "triggered_at": (
                        alert.triggered_at.isoformat() if alert.triggered_at else None
                    ),
                    "acknowledged": alert.acknowledged,
                }
            )

        return success_response(
            data=paginated_response(alert_list, page, per_page, alerts.total)
        )

    except Exception as e:
        return error_response("Failed to fetch alerts", 500, str(e))


@alerts_bp.route("/<int:alert_id>/acknowledge", methods=["PUT"])
@guardian_required
def acknowledge_alert(guardian, alert_id):
    try:
        alert = EmergencyAlert.query.get(alert_id)

        if not alert:
            return error_response("Alert not found", 404)

        alert.acknowledged = True
        db.session.commit()

        return success_response(message="Alert acknowledged successfully")

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to acknowledge alert", 500, str(e))


@alerts_bp.route("/unacknowledged", methods=["GET"])
@guardian_required
def get_unacknowledged_alerts(guardian):
    try:
        vip_id = request.args.get("vip_id", type=int)

        query = EmergencyAlert.query.filter_by(acknowledged=False)

        if vip_id:
            query = query.filter_by(vip_id=vip_id)

        alerts = query.order_by(EmergencyAlert.triggered_at.desc()).all()

        alert_list = []
        for alert in alerts:
            alert_list.append(
                {
                    "alert_id": alert.alert_id,
                    "vip_id": alert.vip_id,
                    "location_id": alert.location_id,
                    "latitude": float(alert.location.latitude),
                    "longitude": float(alert.location.longitude),
                    "location": alert.location.location,
                    "triggered_at": (
                        alert.triggered_at.isoformat() if alert.triggered_at else None
                    ),
                }
            )

        return success_response(data=alert_list)

    except Exception as e:
        return error_response("Failed to fetch unacknowledged alerts", 500, str(e))
