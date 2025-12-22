from flask import Blueprint, request
from app import db
from app.models import VIP, VIPGuardian, Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response

vip_bp = Blueprint("vip", __name__)


@vip_bp.route("/my-vip", methods=["GET"])
@guardian_required
def get_my_vip(guardian):
    """Get the VIP associated with current guardian"""
    try:
        # Get VIP associated with current guardian
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).first()

        if not vip_guardian:
            return error_response("No VIP associated with your account", 404)

        vip = VIP.query.get(vip_guardian.vip_id)

        if not vip:
            return error_response("VIP not found", 404)

        # Get condition/medical info (you might need to add a medical_info table)
        # For now, we'll return a placeholder
        vip_data = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "email": "",  # VIP might not have email in your model
            "avatar": vip.vip_image_url,
            "fullName": vip.vip_name,
            "cellphone": "",  # VIP might not have phone in your model
            "gender": "",  # Add gender field to VIP model if needed
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}",
            "condition": "Visually Impaired",  # Placeholder - add medical condition field
            "province": vip.province,
            "city": vip.city,
            "barangay": vip.barangay,
            "street_address": vip.street_address,
            "relationship": vip_guardian.relationship_to_vip,
        }

        return success_response(data=vip_data)

    except Exception as e:
        return error_response("Failed to fetch VIP profile", 500, str(e))


@vip_bp.route("/my-vip", methods=["PUT"])
@guardian_required
def update_my_vip(guardian):
    """Update the VIP associated with current guardian"""
    try:
        # Check if guardian has VIP access
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).first()

        if not vip_guardian:
            return error_response("No VIP associated with your account", 403)

        vip = VIP.query.get(vip_guardian.vip_id)

        if not vip:
            return error_response("VIP not found", 404)

        data = request.get_json()

        # Update VIP fields
        if "fullName" in data or "name" in data:
            vip.vip_name = data.get("fullName") or data.get("name") or vip.vip_name

        if "avatar" in data:
            vip.vip_image_url = data["avatar"]

        # Update address fields
        if "province" in data:
            vip.province = data["province"]
        if "city" in data:
            vip.city = data["city"]
        if "barangay" in data:
            vip.barangay = data["barangay"]
        if "street_address" in data:
            vip.street_address = data["street_address"]
        elif "address" in data:
            # If address is a single string, parse it or store as is
            vip.street_address = data["address"]

        # Update relationship if provided
        if "relationship" in data:
            vip_guardian.relationship_to_vip = data["relationship"]

        # Update condition/medical info (you might need separate medical_info table)
        # For now, this is a placeholder

        db.session.commit()

        # Return updated VIP data
        updated_vip = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "avatar": vip.vip_image_url,
            "fullName": vip.vip_name,
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}",
            "condition": "Visually Impaired",  # Placeholder
            "relationship": vip_guardian.relationship_to_vip,
        }

        return success_response(
            data=updated_vip, message="VIP profile updated successfully"
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update VIP profile", 500, str(e))


# Keep your existing routes for backward compatibility
@vip_bp.route("", methods=["GET"])
@guardian_required
def get_all_vips(guardian):
    """Get all VIPs (for admin or multiple VIPs per guardian)"""
    try:
        # Get VIPs associated with current guardian
        vip_guardians = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).all()

        vip_list = []
        for vg in vip_guardians:
            vip = VIP.query.get(vg.vip_id)
            if vip:
                vip_list.append(
                    {
                        "vip_id": vip.vip_id,
                        "vip_name": vip.vip_name,
                        "vip_image_url": vip.vip_image_url,
                        "province": vip.province,
                        "city": vip.city,
                        "barangay": vip.barangay,
                        "street_address": vip.street_address,
                        "relationship": vg.relationship_to_vip,
                        "created_at": (
                            vip.created_at.isoformat() if vip.created_at else None
                        ),
                    }
                )

        return success_response(data=vip_list)

    except Exception as e:
        return error_response("Failed to fetch VIPs", 500, str(e))
