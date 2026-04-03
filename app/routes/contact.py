from flask import Blueprint, request, jsonify
from app import db
from app.models import GuardianConcern
from datetime import datetime, timezone

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/', methods=['POST'])
def submit_contact():
    """
    Public endpoint for the contact form.
    Expects JSON: { "name": "...", "email": "...", "message": "..." }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid request, JSON expected'}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    new_concern = GuardianConcern(
        name=name,
        email=email,
        message=message,
        status='unread',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        db.session.add(new_concern)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500