from app import db
from app.models import AccountHistory
from datetime import datetime, timezone


def log_action(guardian_id, action, description):
    """
    Logs a guardian action to account_history_tbl.
    
    action: 'CREATE', 'UPDATE', 'DELETE', 'PAIR', 'UNPAIR', 
            'INVITE', 'REMOVE_GUARDIAN', 'UPDATE_ROLE', etc.
    description: Human-readable string e.g. "Juan Dela Cruz updated VIP profile for Maria Santos"
    """
    try:
        log = AccountHistory(
            guardian_id=guardian_id,
            action=action,
            description=description,
        )
        db.session.add(log)
        # No commit here — let the calling route commit
    except Exception as e:
        print(f"[HISTORY LOG ERROR]: {e}")