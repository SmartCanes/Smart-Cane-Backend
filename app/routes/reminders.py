from flask import Blueprint, request
from app import db
from app.models import NoteReminder
from app.utils.auth import guardian_required
from app.utils.responses import success_response, error_response, paginated_response
from app.utils.auth import guardian_with_device_required

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('', methods=['POST'])
@guardian_required
@guardian_with_device_required
def create_reminder(guardian, devices):
    try:
        data = request.get_json()
        
        required_fields = ['vip_id', 'message', 'reminder_time']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}", 400)
        
        reminder = NoteReminder(
            guardian_id=guardian.guardian_id,
            vip_id=data['vip_id'],
            message=data['message'],
            reminder_time=data['reminder_time'],
            is_active=data.get('is_active', True)
        )
        
        db.session.add(reminder)
        db.session.commit()
        
        return success_response(
            data={"note_reminder_id": reminder.note_reminder_id},
            message="Reminder created successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create reminder", 500, str(e))

@reminders_bp.route('', methods=['GET'])
@guardian_required
def get_reminders(guardian):
    try:
        vip_id = request.args.get('vip_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = NoteReminder.query.filter_by(guardian_id=guardian.guardian_id)
        
        if vip_id:
            query = query.filter_by(vip_id=vip_id)
        
        reminders = query.order_by(
            NoteReminder.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        reminder_list = []
        for reminder in reminders.items:
            reminder_list.append({
                "note_reminder_id": reminder.note_reminder_id,
                "guardian_id": reminder.guardian_id,
                "vip_id": reminder.vip_id,
                "message": reminder.message,
                "reminder_time": reminder.reminder_time.strftime('%H:%M:%S') if reminder.reminder_time else None,
                "is_active": reminder.is_active,
                "created_at": reminder.created_at.isoformat() if reminder.created_at else None
            })
        
        return success_response(
            data=paginated_response(reminder_list, page, per_page, reminders.total)
        )
        
    except Exception as e:
        return error_response("Failed to fetch reminders", 500, str(e))

@reminders_bp.route('/<int:reminder_id>', methods=['PUT'])
@guardian_required
def update_reminder(guardian, reminder_id):
    try:
        reminder = NoteReminder.query.get(reminder_id)
        
        if not reminder:
            return error_response("Reminder not found", 404)
        
        if reminder.guardian_id != guardian.guardian_id:
            return error_response("Unauthorized to update this reminder", 403)
        
        data = request.get_json()
        
        if data.get('message'):
            reminder.message = data['message']
        if data.get('reminder_time'):
            reminder.reminder_time = data['reminder_time']
        if 'is_active' in data:
            reminder.is_active = data['is_active']
        
        db.session.commit()
        
        return success_response(message="Reminder updated successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update reminder", 500, str(e))

@reminders_bp.route('/<int:reminder_id>', methods=['DELETE'])
@guardian_required
def delete_reminder(guardian, reminder_id):
    try:
        reminder = NoteReminder.query.get(reminder_id)
        
        if not reminder:
            return error_response("Reminder not found", 404)
        
        if reminder.guardian_id != guardian.guardian_id:
            return error_response("Unauthorized to delete this reminder", 403)
        
        db.session.delete(reminder)
        db.session.commit()
        
        return success_response(message="Reminder deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete reminder", 500, str(e))