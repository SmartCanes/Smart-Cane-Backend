from app import db
from app.models import AccountHistory
from datetime import datetime, timezone


def log_action(guardian_id, action, description, device_id=None):
    """
    Logs a guardian action to account_history_tbl.

    action: 'CREATE', 'UPDATE', 'DELETE', 'PAIR', 'UNPAIR',
            'INVITE', 'REMOVE_GUARDIAN', 'UPDATE_ROLE', etc.
    description: Human-readable string e.g. "Juan Dela Cruz updated VIP profile for Maria Santos"
    """
    try:
        entry = AccountHistory(
            guardian_id=guardian_id,
            action=action,
            description=description,
            device_id=device_id,  # NEW
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(entry)
    except Exception as e:
        db.session.rollback()
        print(f"[history_logger] Failed to log action: {e}")
