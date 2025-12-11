from flask import Blueprint, request
from app import db
from app.models import Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response

guardian_bp = Blueprint('guardian', __name__)

@guardian_bp.route('', methods=['GET'])
@guardian_required
def get_guardians_by_vip(guardian):
    try:
        vip_id = request.args.get('vip_id', type=int)
        
        if not vip_id:
            return error_response("VIP ID is required", 400)
        
        guardians = Guardian.query.filter_by(vip_id=vip_id).all()
        
        guardian_list = []
        for g in guardians:
            guardian_list.append({
                "guardian_id": g.guardian_id,
                "username": g.username,
                "guardian_name": g.guardian_name,
                "email": g.email,
                "contact_number": g.contact_number,
                "relationship_to_vip": g.relationship_to_vip,
                "guardian_image_url": g.guardian_image_url,
                "created_at": g.created_at.isoformat() if g.created_at else None
            })
        
        return success_response(data=guardian_list)
        
    except Exception as e:
        return error_response("Failed to fetch guardians", 500, str(e))

@guardian_bp.route('/<int:guardian_id>', methods=['GET'])
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
            "created_at": guardian_data.created_at.isoformat() if guardian_data.created_at else None
        }
        
        return success_response(data=guardian_info)
        
    except Exception as e:
        return error_response("Failed to fetch guardian", 500, str(e))

@guardian_bp.route('/<int:guardian_id>', methods=['PUT'])
@guardian_required
def update_guardian(guardian, guardian_id):
    try:
        # Guardians can only update their own profile
        if guardian.guardian_id != guardian_id:
            return error_response("Unauthorized to update this profile", 403)
        
        data = request.get_json()
        
        if data.get('email'):
            existing_guardian = Guardian.query.filter(
                Guardian.email == data['email'],
                Guardian.guardian_id != guardian_id
            ).first()
            if existing_guardian:
                return error_response("Email already exists", 400)
        
        if data.get('username'):
            existing_guardian = Guardian.query.filter(
                Guardian.username == data['username'],
                Guardian.guardian_id != guardian_id
            ).first()
            if existing_guardian:
                return error_response("Username already exists", 400)
        
        updatable_fields = [
            'guardian_name', 'email', 'contact_number',
            'province', 'city', 'barangay', 'village', 'street_address', 'guardian_image_url'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(guardian, field, data[field])
        
        if data.get('password'):
            guardian.set_password(data['password'])
        
        db.session.commit()
        
        return success_response(message="Guardian updated successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update guardian", 500, str(e))