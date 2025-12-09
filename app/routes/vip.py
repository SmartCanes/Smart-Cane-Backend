from flask import Blueprint, request
from app import db
from app.models import VIP, VIPGuardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response, paginated_response

vip_bp = Blueprint('vip', __name__)

@vip_bp.route('', methods=['POST'])
@guardian_required
def create_vip(guardian):
    try:
        data = request.get_json()
        
        if not data.get('vip_name'):
            return error_response("VIP name is required", 400)
        
        vip = VIP(
            vip_name=data['vip_name'],
            vip_image_url=data.get('vip_image_url'),
            province=data.get('province'),
            city=data.get('city'),
            barangay=data.get('barangay'),
            street_address=data.get('street_address')
        )
        
        db.session.add(vip)
        db.session.commit()
        
        # Create the VIP–Guardian association
        vip_guardian = VIPGuardian(
            vip_id=vip.vip_id,
            guardian_id=guardian.guardian_id,
            relationship_to_vip=data.get('relationship_to_vip')  # optional field
        )
        db.session.add(vip_guardian)
        db.session.commit()
        
        return success_response(
            data={"vip_id": vip.vip_id},
            message="VIP created successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create VIP", 500, str(e))
    
@vip_bp.route('', methods=['GET'])
@guardian_required
def get_all_vips(guardian):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        vips = VIP.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        vip_list = []
        for vip in vips.items:
            vip_list.append({
                "vip_id": vip.vip_id,
                "vip_name": vip.vip_name,
                "vip_image_url": vip.vip_image_url,
                "province": vip.province,
                "city": vip.city,
                "barangay": vip.barangay,
                "street_address": vip.street_address,
                "created_at": vip.created_at.isoformat() if vip.created_at else None
            })
        
        return success_response(
            data=paginated_response(vip_list, page, per_page, vips.total)
        )
        
    except Exception as e:
        return error_response("Failed to fetch VIPs", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['GET'])
@guardian_required
def get_vip(guardian, vip_id):
    try:
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        vip_data = {
            "vip_id": vip.vip_id,
            "vip_name": vip.vip_name,
            "vip_image_url": vip.vip_image_url,
            "province": vip.province,
            "city": vip.city,
            "barangay": vip.barangay,
            "street_address": vip.street_address,
            "created_at": vip.created_at.isoformat() if vip.created_at else None
        }
        
        return success_response(data=vip_data)
        
    except Exception as e:
        return error_response("Failed to fetch VIP", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['PUT'])
@guardian_required
def update_vip(guardian, vip_id):
    try:
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        data = request.get_json()
        
        if data.get('vip_name'):
            vip.vip_name = data['vip_name']
        if 'vip_image_url' in data:
            vip.vip_image_url = data['vip_image_url']
        if 'province' in data:
            vip.province = data['province']
        if 'city' in data:
            vip.city = data['city']
        if 'barangay' in data:
            vip.barangay = data['barangay']
        if 'street_address' in data:
            vip.street_address = data['street_address']
        
        db.session.commit()
        
        return success_response(message="VIP updated successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update VIP", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['DELETE'])
@guardian_required
def delete_vip(guardian, vip_id):
    try:
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        db.session.delete(vip)
        db.session.commit()
        
        return success_response(message="VIP deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete VIP", 500, str(e))