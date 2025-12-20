from flask import Blueprint, request
from app import db
from app.models import Guardian, VIPGuardian, VIP
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt_identity

guardian_bp = Blueprint("guardian", __name__)

# ========== NEW ENDPOINTS FOR PROFILE MANAGEMENT ==========


@guardian_bp.route("/profile", methods=["GET"])
@guardian_required
def get_my_profile(guardian):
    """Get current logged-in guardian's profile"""
    try:
        # The 'guardian' parameter is injected by @guardian_required decorator
        guardian_info = {
            "id": guardian.guardian_id,
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name or guardian.username,
            "guardian_name": guardian.guardian_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "cellphone": guardian.contact_number,  # Alias for frontend
            "guardian_image_url": guardian.guardian_image_url,
            "avatar": guardian.guardian_image_url,  # Alias for frontend
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "village": guardian.village,
            "street_address": guardian.street_address,
            "address": f"{guardian.street_address or ''}, {guardian.barangay or ''}, {guardian.city or ''}, {guardian.province or ''}",
            "role": guardian.role,
            "created_at": (
                guardian.created_at.isoformat() if guardian.created_at else None
            ),
            "updated_at": (
                guardian.updated_at.isoformat() if guardian.updated_at else None
            ),
        }

        return success_response(data=guardian_info)

    except Exception as e:
        print(e)
        return error_response("Failed to fetch guardian profile", 500, str(e))


@guardian_bp.route("/profile", methods=["PUT"])
@guardian_required
def update_my_profile(guardian):
    """Update current logged-in guardian's profile"""
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response("Invalid JSON payload", 400)

        # Check if email already exists (excluding current guardian)
        if "email" in data and data["email"] != guardian.email:
            existing_guardian = Guardian.query.filter_by(email=data["email"]).first()
            if existing_guardian:
                return error_response("Email already exists", 400)

        # Check if username already exists (excluding current guardian)
        if "username" in data and data["username"] != guardian.username:
            existing_guardian = Guardian.query.filter_by(
                username=data["username"]
            ).first()
            if existing_guardian:
                return error_response("Username already exists", 400)

        # Update fields from frontend data
        # Map frontend field names to model field names
        field_mapping = {
            "fullName": "guardian_name",
            "name": "guardian_name",
            "guardian_name": "guardian_name",
            "email": "email",
            "cellphone": "contact_number",
            "contact_number": "contact_number",
            "avatar": "guardian_image_url",
            "guardian_image_url": "guardian_image_url",
            "province": "province",
            "city": "city",
            "barangay": "barangay",
            "village": "village",
            "street_address": "street_address",
            "address": "street_address",  # Map address to street_address
        }

        for frontend_field, model_field in field_mapping.items():
            if frontend_field in data:
                # Handle address specially if it's a combined string
                if frontend_field == "address" and isinstance(
                    data[frontend_field], str
                ):
                    # Store the full address as street_address
                    setattr(guardian, model_field, data[frontend_field])
                elif data[frontend_field] is not None:
                    setattr(guardian, model_field, data[frontend_field])

        # Update password if provided
        if "password" in data and data["password"]:
            guardian.set_password(data["password"])

        db.session.commit()

        # Return updated profile
        updated_info = {
            "id": guardian.guardian_id,
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name or guardian.username,
            "guardian_name": guardian.guardian_name,
            "email": guardian.email,
            "contact_number": guardian.contact_number,
            "cellphone": guardian.contact_number,
            "guardian_image_url": guardian.guardian_image_url,
            "avatar": guardian.guardian_image_url,
            "province": guardian.province,
            "city": guardian.city,
            "barangay": guardian.barangay,
            "village": guardian.village,
            "street_address": guardian.street_address,
            "address": f"{guardian.street_address or ''}, {guardian.barangay or ''}, {guardian.city or ''}, {guardian.province or ''}",
            "role": guardian.role,
        }

        return success_response(
            data=updated_info, message="Profile updated successfully"
        )

    except Exception as e:
        db.session.rollback()
        print("UPDATE PROFILE ERROR:", e)
        return error_response("Failed to update profile", 500, str(e))


@guardian_bp.route("/vip-guardians", methods=["GET"])
@guardian_required
def get_vip_guardians(guardian):
    """Get all guardians associated with the same VIPs as current guardian"""
    try:
        # Get all VIPs associated with current guardian
        vip_guardians = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id
        ).all()
        vip_ids = [vg.vip_id for vg in vip_guardians]

        if not vip_ids:
            return success_response(data=[])

        # Get all guardians for these VIPs
        all_vip_guardians = VIPGuardian.query.filter(
            VIPGuardian.vip_id.in_(vip_ids)
        ).all()
        guardian_ids = [vg.guardian_id for vg in all_vip_guardians]

        # Exclude current guardian from the list
        guardian_ids = [gid for gid in guardian_ids if gid != guardian.guardian_id]

        if not guardian_ids:
            return success_response(data=[])

        # Get guardian details
        guardians = Guardian.query.filter(Guardian.guardian_id.in_(guardian_ids)).all()

        guardian_list = []
        for g in guardians:
            # Get relationship info from VIPGuardian table
            vip_guardian = VIPGuardian.query.filter_by(
                guardian_id=g.guardian_id,
                vip_id=vip_ids[0],  # Get relationship from first VIP
            ).first()

            guardian_info = {
                "id": g.guardian_id,
                "guardian_id": g.guardian_id,
                "username": g.username,
                "name": g.guardian_name or g.username,
                "guardian_name": g.guardian_name,
                "fullName": g.guardian_name,  # Alias for frontend
                "email": g.email,
                "contact_number": g.contact_number,
                "cellphone": g.contact_number,  # Alias for frontend
                "guardian_image_url": g.guardian_image_url,
                "avatar": g.guardian_image_url,  # Alias for frontend
                "province": g.province,
                "city": g.city,
                "barangay": g.barangay,
                "village": g.village,
                "street_address": g.street_address,
                "address": f"{g.street_address or ''}, {g.barangay or ''}, {g.city or ''}, {g.province or ''}",
                "relationship": (
                    vip_guardian.relationship_to_vip if vip_guardian else None
                ),
                "created_at": g.created_at.isoformat() if g.created_at else None,
                "updated_at": g.updated_at.isoformat() if g.updated_at else None,
            }
            guardian_list.append(guardian_info)

        return success_response(data=guardian_list)

    except Exception as e:
        return error_response("Failed to fetch VIP guardians", 500, str(e))


# ========== EXISTING ENDPOINTS (KEEP THESE) ==========


@guardian_bp.route("", methods=["GET"])
@guardian_required
def get_guardians_by_vip(guardian):
    try:
        vip_id = request.args.get("vip_id", type=int)

        if not vip_id:
            return error_response("VIP ID is required", 400)

        guardians = Guardian.query.filter_by(vip_id=vip_id).all()

        guardian_list = []
        for g in guardians:
            guardian_list.append(
                {
                    "guardian_id": g.guardian_id,
                    "username": g.username,
                    "guardian_name": g.guardian_name,
                    "email": g.email,
                    "contact_number": g.contact_number,
                    "relationship_to_vip": g.relationship_to_vip,
                    "guardian_image_url": g.guardian_image_url,
                    "created_at": g.created_at.isoformat() if g.created_at else None,
                }
            )

        return success_response(data=guardian_list)

    except Exception as e:
        return error_response("Failed to fetch guardians", 500, str(e))


@guardian_bp.route("/<int:guardian_id>", methods=["GET"])
@guardian_required
def get_guardian(guardian, guardian_id):
    try:
        guardian_data = Guardian.query.get(guardian_id)

        if not guardian_data:
            return error_response("Guardian not found", 404)

        guardian_info = {
            "guardian_id": guardian_data.guardian_id,
            "username": guardian_data.username,
            "guardian_name": guardian_data.guardian_name,
            "email": guardian_data.email,
            "contact_number": guardian_data.contact_number,
            "relationship_to_vip": guardian_data.relationship_to_vip,
            "province": guardian_data.province,
            "city": guardian_data.city,
            "barangay": guardian_data.barangay,
            "street_address": guardian_data.street_address,
            "guardian_image_url": guardian_data.guardian_image_url,
            "created_at": (
                guardian_data.created_at.isoformat()
                if guardian_data.created_at
                else None
            ),
        }

        return success_response(data=guardian_info)

    except Exception as e:
        return error_response("Failed to fetch guardian", 500, str(e))


@guardian_bp.route("/<int:guardian_id>", methods=["PUT"])
@guardian_required
def update_guardian(guardian, guardian_id):
    try:
        # Guardians can only update their own profile
        if guardian.guardian_id != guardian_id:
            return error_response("Unauthorized to update this profile", 403)

        data = request.get_json()

        if data.get("email"):
            existing_guardian = Guardian.query.filter(
                Guardian.email == data["email"], Guardian.guardian_id != guardian_id
            ).first()
            if existing_guardian:
                return error_response("Email already exists", 400)

        if data.get("username"):
            existing_guardian = Guardian.query.filter(
                Guardian.username == data["username"],
                Guardian.guardian_id != guardian_id,
            ).first()
            if existing_guardian:
                return error_response("Username already exists", 400)

        updatable_fields = [
            "guardian_name",
            "email",
            "contact_number",
            "province",
            "city",
            "barangay",
            "village",
            "street_address",
            "guardian_image_url",
        ]

        for field in updatable_fields:
            if field in data:
                setattr(guardian, field, data[field])

        if data.get("password"):
            guardian.set_password(data["password"])

        db.session.commit()

        return success_response(message="Guardian updated successfully")

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update guardian", 500, str(e))


# ========== EXTRA HELPER ENDPOINT ==========


@guardian_bp.route("/test", methods=["GET"])
@guardian_required
def test_endpoint(guardian):
    """Test endpoint to verify guardian authentication is working"""
    return success_response(
        message="Guardian endpoint is working",
        data={
            "guardian_id": guardian.guardian_id,
            "username": guardian.username,
            "name": guardian.guardian_name,
        },
    )
