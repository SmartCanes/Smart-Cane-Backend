from flask import Blueprint, request, current_app
from app import db
from app.models import VIP, VIPGuardian, Guardian
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os
import uuid

vip_bp = Blueprint("vip", __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@vip_bp.route('/<int:vip_id>/image', methods=['POST'])
@guardian_required
def upload_vip_image(guardian, vip_id):
    try:
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id,
            vip_id=vip_id
        ).first()
        
        if not vip_guardian:
            return error_response("No access to this VIP", 403)
        
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        if 'image' not in request.files:
            return error_response("No image file provided", 400)
        
        file = request.files['image']
        
        if file.filename == '':
            return error_response("No selected file", 400)
        
        if not allowed_file(file.filename):
            return error_response("File type not allowed. Only PNG, JPG, JPEG, GIF, WEBP are allowed", 400)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        new_filename = f"vip_{vip.vip_id}_{timestamp}_{unique_id}.{file_extension}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        upload_path = os.path.join(upload_folder, 'vip_profiles')
        
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, new_filename)
        
        file.save(file_path)
        
        if not os.path.exists(file_path):
            return error_response("Failed to save image file", 500)
        
        if vip.vip_image_url:
            old_image_path = vip.vip_image_url
            if 'uploads/' in old_image_path:
                old_image_path = old_image_path.split('uploads/')[-1]
            
            full_old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_path)
            
            if os.path.exists(full_old_path):
                try:
                    os.remove(full_old_path)
                except Exception:
                    pass
        
        relative_path = f"vip_profiles/{new_filename}"
        vip.vip_image_url = relative_path
        vip.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        base_url = request.host_url.rstrip('/')
        image_url = f"{base_url}/uploads/{relative_path}"
        
        return success_response(
            data={
                "image_url": image_url,
                "relative_path": relative_path,
                "avatar": image_url,
                "vip_image_url": image_url
            },
            message="VIP profile image uploaded successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to upload VIP image", 500, str(e))

@vip_bp.route('/my-vip', methods=['GET'])
@guardian_required
def get_my_vip(guardian):
    try:
        vip_guardian = VIPGuardian.query.filter_by(guardian_id=guardian.guardian_id).first()
        
        if not vip_guardian:
            return error_response("No VIP associated with your account", 404)

        vip = VIP.query.get(vip_guardian.vip_id)

        if not vip:
            return error_response("VIP not found", 404)
        
        vip_data = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "fullName": vip.vip_name,
            "avatar": vip.vip_image_url or "",
            "province": vip.province or "",
            "city": vip.city or "",
            "barangay": vip.barangay or "",
            "street_address": vip.street_address or "",
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}".strip(", "),
            "relationship": vip_guardian.relationship_to_vip or "",
            "created_at": vip.created_at.isoformat() if vip.created_at else None,
            "updated_at": vip.updated_at.isoformat() if vip.updated_at else None
        }

        return success_response(data=vip_data)

    except Exception as e:
        return error_response("Failed to fetch VIP profile", 500, str(e))


@vip_bp.route("/my-vip", methods=["PUT"])
@guardian_required
def update_my_vip(guardian):
    try:
        vip_guardian = VIPGuardian.query.filter_by(guardian_id=guardian.guardian_id).first()
        
        if not vip_guardian:
            return error_response("No VIP associated with your account", 403)

        vip = VIP.query.get(vip_guardian.vip_id)

        if not vip:
            return error_response("VIP not found", 404)

        data = request.get_json()
        
        if 'fullName' in data or 'name' in data:
            vip.vip_name = data.get('fullName') or data.get('name') or vip.vip_name
        
        if 'avatar' in data:
            vip.vip_image_url = data['avatar']

        if 'province' in data:
            vip.province = data['province']
        if 'city' in data:
            vip.city = data['city']
        if 'barangay' in data:
            vip.barangay = data['barangay']
        if 'street_address' in data:
            vip.street_address = data['street_address']

        if 'relationship' in data:
            vip_guardian.relationship_to_vip = data['relationship']
        
        vip.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        updated_vip = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "fullName": vip.vip_name,
            "avatar": vip.vip_image_url or "",
            "province": vip.province or "",
            "city": vip.city or "",
            "barangay": vip.barangay or "",
            "street_address": vip.street_address or "",
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}".strip(", "),
            "relationship": vip_guardian.relationship_to_vip or "",
            "updated_at": vip.updated_at.isoformat() if vip.updated_at else None
        }

        return success_response(
            data=updated_vip, message="VIP profile updated successfully"
        )

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update VIP profile", 500, str(e))

@vip_bp.route('', methods=['POST'])
@guardian_required
def create_vip(guardian):
    try:
        data = request.get_json()

        required_fields = ['name', 'province', 'city', 'barangay']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)
        
        existing_vip = VIPGuardian.query.filter_by(guardian_id=guardian.guardian_id).first()
        if existing_vip:
            return error_response("You already have a VIP associated with your account", 400)
        
        new_vip = VIP(
            vip_name=data.get('fullName') or data.get('name'),
            vip_image_url=data.get('avatar', ''),
            province=data.get('province'),
            city=data.get('city'),
            barangay=data.get('barangay'),
            street_address=data.get('street_address', ''),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_vip)
        db.session.flush() 
        
        vip_guardian = VIPGuardian(
            vip_id=new_vip.vip_id,
            guardian_id=guardian.guardian_id,
            relationship_to_vip=data.get('relationship', 'Guardian'),
            assigned_at=datetime.utcnow()
        )
        
        db.session.add(vip_guardian)
        db.session.commit()
        
        vip_data = {
            "id": new_vip.vip_id,
            "name": new_vip.vip_name,
            "fullName": new_vip.vip_name,
            "avatar": new_vip.vip_image_url or "",
            "province": new_vip.province,
            "city": new_vip.city,
            "barangay": new_vip.barangay,
            "street_address": new_vip.street_address or "",
            "address": f"{new_vip.street_address or ''}, {new_vip.barangay or ''}, {new_vip.city or ''}, {new_vip.province or ''}".strip(", "),
            "relationship": vip_guardian.relationship_to_vip,
            "created_at": new_vip.created_at.isoformat() if new_vip.created_at else None
        }
        
        return success_response(
            data=vip_data,
            message="VIP created successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create VIP", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['GET'])
@guardian_required
def get_vip_by_id(guardian, vip_id):
    try:
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id,
            vip_id=vip_id
        ).first()
        
        if not vip_guardian:
            return error_response("No access to this VIP", 403)
        
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        vip_data = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "fullName": vip.vip_name,
            "avatar": vip.vip_image_url or "",
            "province": vip.province or "",
            "city": vip.city or "",
            "barangay": vip.barangay or "",
            "street_address": vip.street_address or "",
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}".strip(", "),
            "relationship": vip_guardian.relationship_to_vip or "",
            "created_at": vip.created_at.isoformat() if vip.created_at else None,
            "updated_at": vip.updated_at.isoformat() if vip.updated_at else None
        }
        
        return success_response(data=vip_data)
        
    except Exception as e:
        return error_response("Failed to fetch VIP", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['PUT'])
@guardian_required
def update_vip_by_id(guardian, vip_id):
    try:
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id,
            vip_id=vip_id
        ).first()
        
        if not vip_guardian:
            return error_response("No access to this VIP", 403)
        
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        data = request.get_json()
        
        if 'fullName' in data or 'name' in data:
            vip.vip_name = data.get('fullName') or data.get('name') or vip.vip_name
        
        if 'avatar' in data:
            vip.vip_image_url = data['avatar']

        if 'province' in data:
            vip.province = data['province']
        if 'city' in data:
            vip.city = data['city']
        if 'barangay' in data:
            vip.barangay = data['barangay']
        if 'street_address' in data:
            vip.street_address = data['street_address']
        
        if 'relationship' in data:
            vip_guardian.relationship_to_vip = data['relationship']
        
        vip.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        updated_vip = {
            "id": vip.vip_id,
            "name": vip.vip_name,
            "fullName": vip.vip_name,
            "avatar": vip.vip_image_url or "",
            "province": vip.province or "",
            "city": vip.city or "",
            "barangay": vip.barangay or "",
            "street_address": vip.street_address or "",
            "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}".strip(", "),
            "relationship": vip_guardian.relationship_to_vip or "",
            "updated_at": vip.updated_at.isoformat() if vip.updated_at else None
        }
        
        return success_response(
            data=updated_vip,
            message="VIP updated successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update VIP", 500, str(e))

@vip_bp.route('/<int:vip_id>', methods=['DELETE'])
@guardian_required
def delete_vip(guardian, vip_id):
    try:
        vip_guardian = VIPGuardian.query.filter_by(
            guardian_id=guardian.guardian_id,
            vip_id=vip_id
        ).first()
        
        if not vip_guardian:
            return error_response("No access to this VIP", 403)
        
        vip = VIP.query.get(vip_id)
        
        if not vip:
            return error_response("VIP not found", 404)
        
        db.session.delete(vip_guardian)
        db.session.flush()
        
        other_associations = VIPGuardian.query.filter_by(vip_id=vip_id).count()
        
        if other_associations == 0:
            db.session.delete(vip)
            message = "VIP profile deleted successfully"
        else:
            message = "VIP association removed successfully"
        
        db.session.commit()
        
        return success_response(
            message=message,
            status_code=200
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete VIP", 500, str(e))

@vip_bp.route('', methods=['GET'])
@guardian_required
def get_all_vips(guardian):
    try:
        vip_guardians = VIPGuardian.query.filter_by(guardian_id=guardian.guardian_id).all()
        
        vip_list = []
        for vg in vip_guardians:
            vip = VIP.query.get(vg.vip_id)
            if vip:
                vip_list.append({
                    "id": vip.vip_id,
                    "name": vip.vip_name,
                    "fullName": vip.vip_name,
                    "avatar": vip.vip_image_url or "",
                    "province": vip.province or "",
                    "city": vip.city or "",
                    "barangay": vip.barangay or "",
                    "street_address": vip.street_address or "",
                    "address": f"{vip.street_address or ''}, {vip.barangay or ''}, {vip.city or ''}, {vip.province or ''}".strip(", "),
                    "relationship": vg.relationship_to_vip or "",
                    "created_at": vip.created_at.isoformat() if vip.created_at else None,
                    "updated_at": vip.updated_at.isoformat() if vip.updated_at else None,
                    "assigned_at": vg.assigned_at.isoformat() if vg.assigned_at else None
                })
        
        return success_response(data=vip_list)

    except Exception as e:
        return error_response("Failed to fetch VIPs", 500, str(e))
