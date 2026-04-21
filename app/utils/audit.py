import json
from flask import request
from app import db
from app.models import AdminAuditLog


def log_audit(
    actor_admin_id,
    action_type,
    reason_code="system",
    reason_text="",
    target_admin_id=None,
    target_concern_id=None,
    old_value=None,
    new_value=None,
    status="success",
    failure_message=None,
):
    db.session.add(
        AdminAuditLog(
            actor_admin_id=actor_admin_id,
            target_admin_id=target_admin_id,
            target_concern_id=target_concern_id,
            action_type=action_type,
            old_value_json=json.dumps(old_value) if old_value is not None else None,
            new_value_json=json.dumps(new_value) if new_value is not None else None,
            reason_code=reason_code,
            reason_text=reason_text,
            status=status,
            failure_message=failure_message,
            ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
            user_agent=(request.user_agent.string or "")[:255],
        )
    )
