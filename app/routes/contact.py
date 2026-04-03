from flask import Blueprint, request, jsonify
from app import db
from app.models import GuardianConcern
from datetime import datetime, timezone

contact_bp = Blueprint('contact', __name__)

# Lightweight in-memory throttle to complement frontend cooldown.
# Keyed by client IP + email, with progressive waiting windows.
CONTACT_SUBMISSION_STATE = {}


def _get_client_ip():
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def _check_rate_limit(rate_key, now_ts):
    state = CONTACT_SUBMISSION_STATE.get(rate_key, {'count': 0, 'last_sent_ts': 0})
    count = int(state.get('count', 0) or 0)
    last_sent_ts = float(state.get('last_sent_ts', 0) or 0)

    # Reset progressive penalties after 24 hours of inactivity.
    if last_sent_ts and (now_ts - last_sent_ts) > 86400:
        count = 0
        last_sent_ts = 0

    wait_seconds = 0
    if count == 1:
        wait_seconds = 60
    elif count == 2:
        wait_seconds = 5 * 60
    elif count >= 3:
        wait_seconds = 60 * 60

    if count > 0 and (now_ts - last_sent_ts) < wait_seconds:
        remaining_seconds = int(wait_seconds - (now_ts - last_sent_ts))
        return remaining_seconds

    return 0


def _register_successful_submission(rate_key, now_ts):
    state = CONTACT_SUBMISSION_STATE.get(rate_key, {'count': 0, 'last_sent_ts': 0})
    state['count'] = int(state.get('count', 0) or 0) + 1
    state['last_sent_ts'] = now_ts
    CONTACT_SUBMISSION_STATE[rate_key] = state

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
    source = data.get('source', '').strip()[:50]

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    now_ts = datetime.now(timezone.utc).timestamp()
    rate_key = f"{_get_client_ip()}::{email.lower()}"
    remaining_seconds = _check_rate_limit(rate_key, now_ts)
    if remaining_seconds > 0:
        remaining_minutes = max(1, (remaining_seconds + 59) // 60)
        return jsonify({
            'error': f'Please wait {remaining_minutes} minute(s) before sending another concern.',
            'retry_after_seconds': remaining_seconds,
        }), 429

    stored_message = message
    if source:
        stored_message = f"[Source: {source}]\n\n{message}"

    new_concern = GuardianConcern(
        name=name,
        email=email,
        message=stored_message,
        status='unread',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        db.session.add(new_concern)
        db.session.commit()
        _register_successful_submission(rate_key, now_ts)
        return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500