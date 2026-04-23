from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import GuardianConcern, Admin
from app.models import Notification, NotificationRead
from app.utils.audit import log_audit
from datetime import datetime, timezone
import logging
from sqlalchemy import and_

logger = logging.getLogger(__name__)

concerns_bp = Blueprint("concerns", __name__, url_prefix="/api/guardian-concerns")

ALLOWED_PROCESS_STAGES = {
    "new",
    "acknowledged",
    "ongoing",
    "awaiting_client",
    "escalated",
    "resolved",
    "failed_to_resolve",
}
PROCESS_STAGES_REQUIRING_REMARKS = {"escalated", "failed_to_resolve"}


# Helper: get current admin from JWT
def get_current_admin():
    """Return the Admin instance of the authenticated user."""
    admin_id = get_jwt_identity()
    return Admin.query.get(admin_id)


# Helper: admin access decorator (role: admin or super_admin)
def admin_required(f):
    from functools import wraps

    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        admin = get_current_admin()
        if not admin or admin.role not in ("admin", "super_admin"):
            return jsonify({"error": "Admin access required"}), 403
        g.current_admin = admin   # store for later use if needed
        return f(*args, **kwargs)
    return decorated


# Helper: super admin only decorator
def super_admin_required(f):
    from functools import wraps

    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        admin = get_current_admin()
        if not admin or admin.role != "super_admin":
            return jsonify({"error": "Super admin access required"}), 403
        g.current_admin = admin
        return f(*args, **kwargs)
    return decorated


# GET all concerns (admin only)
@concerns_bp.route("/", methods=["GET"])
@admin_required
def get_concerns():
    try:
        status = request.args.get("status")
        query = GuardianConcern.query.filter_by(is_deleted=False)
        if status and status in ["unread", "read", "resolved"]:
            query = query.filter_by(status=status)
        concerns = query.order_by(GuardianConcern.created_at.desc()).all()
        return jsonify([c.to_dict() for c in concerns])
    except Exception as e:
        logger.exception("Error fetching guardian concerns")
        return jsonify({"error": "Internal server error"}), 500


# PATCH update a concern (admin only)
@concerns_bp.route("/<int:concern_id>", methods=["PATCH"])
@admin_required
def update_concern(concern_id):
    try:
        concern = GuardianConcern.query.filter_by(concern_id=concern_id, is_deleted=False).first()
        if not concern:
            return jsonify({"error": "Concern not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400

        audit_new_value = {}

        # Update status if provided
        if "status" in data:
            new_status = data["status"]
            if new_status not in ("unread", "read", "resolved"):
                return jsonify({"error": "Invalid status"}), 400
            concern.status = new_status
            audit_new_value["status"] = new_status

        # Update admin reply if provided
        if "admin_reply" in data:
            reply_text = str(data["admin_reply"] or "").strip()
            # Only set reply metadata if the reply text is actually provided
            if reply_text:
                concern.admin_reply = reply_text
                # If this is a new reply (was empty), set the admin who replied
                if not concern.replied_by_admin_id:
                    concern.replied_by_admin_id = g.current_admin.admin_id
                    concern.replied_at = datetime.now(timezone.utc)
            else:
                # Clearing the reply text -> also clear metadata
                concern.admin_reply = None
                concern.replied_by_admin_id = None
                concern.replied_at = None
            audit_new_value["admin_reply"] = concern.admin_reply

        process_fields_updated = False

        if "process_stage" in data:
            new_process_stage = str(data["process_stage"] or "").strip().lower()
            if new_process_stage not in ALLOWED_PROCESS_STAGES:
                return jsonify({"error": "Invalid process stage"}), 400
            if concern.process_stage != new_process_stage:
                concern.process_stage = new_process_stage
                process_fields_updated = True
            audit_new_value["process_stage"] = new_process_stage

            # Keep status and process stage aligned even when status is omitted.
            if new_process_stage == "resolved" and "status" not in data:
                concern.status = "resolved"
                audit_new_value["status"] = "resolved"

        if "resolution_remarks" in data:
            raw_remarks = str(data["resolution_remarks"] or "").strip()
            normalized_remarks = raw_remarks if raw_remarks else None
            if concern.resolution_remarks != normalized_remarks:
                concern.resolution_remarks = normalized_remarks
                process_fields_updated = True
            audit_new_value["resolution_remarks"] = normalized_remarks

        if "process_stage" in data or "resolution_remarks" in data:
            effective_stage = (
                str(data.get("process_stage") or concern.process_stage).strip().lower()
            )
            effective_remarks = str(
                data.get("resolution_remarks", concern.resolution_remarks) or ""
            ).strip()
            if (
                effective_stage in PROCESS_STAGES_REQUIRING_REMARKS
                and len(effective_remarks) < 10
            ):
                return jsonify({
                    "error": "Remarks must be at least 10 characters for this process stage"
                }), 400

        if process_fields_updated:
            concern.process_updated_by_admin_id = g.current_admin.admin_id
            concern.process_updated_at = datetime.now(timezone.utc)
            audit_new_value["process_updated_by_admin_id"] = g.current_admin.admin_id
            audit_new_value["process_updated_at"] = concern.process_updated_at.isoformat()

        db.session.commit()

        log_audit(
            actor_admin_id=g.current_admin.admin_id,
            action_type="concern_update",
            reason_code="concern_update",
            reason_text=f"Concern #{concern_id} updated.",
            target_concern_id=concern_id,
            new_value=audit_new_value,
        )
        db.session.commit()

        # Keep notification read-state in sync for the current admin
        if concern.status in ("read", "resolved"):
            n = Notification.query.filter(
                and_(
                    Notification.type == "guardian_concern",
                    Notification.related_concern_id == concern.concern_id,
                )
            ).order_by(Notification.created_at.desc()).first()
            if n:
                existing = NotificationRead.query.filter_by(
                    notification_id=n.notification_id,
                    admin_id=g.current_admin.admin_id,
                ).first()
                if not existing:
                    db.session.add(
                        NotificationRead(
                            notification_id=n.notification_id,
                            admin_id=g.current_admin.admin_id,
                            read_at=datetime.now(timezone.utc),
                        )
                    )
                    db.session.commit()
        return jsonify(concern.to_dict())

    except Exception as e:
        db.session.rollback()
        logger.exception("Error updating concern %s", concern_id)
        return jsonify({"error": "Internal server error"}), 500


# DELETE a concern (super admin only) — soft-delete with full audit trail
@concerns_bp.route("/<int:concern_id>", methods=["DELETE"])
@super_admin_required
def delete_concern(concern_id):
    try:
        data = request.get_json(silent=True) or {}
        reason_code = str(data.get("reason_code", "")).strip() or "other"
        reason_text = str(data.get("reason_text", "")).strip() or "Deleted by admin."

        concern = GuardianConcern.query.filter_by(concern_id=concern_id, is_deleted=False).first()
        if not concern:
            return jsonify({"error": "Concern not found"}), 404

        # --- Step 1: Capture full snapshot BEFORE any mutation ---
        old_value_snapshot = {
            "concern_id":              concern.concern_id,
            "name":                    concern.name,
            "email":                   concern.email,
            "deleted_concern_message": concern.message,
            "status":                  concern.status,
            "admin_reply":             concern.admin_reply,
            "replied_by_admin_id":     concern.replied_by_admin_id,
            "process_stage":           concern.process_stage,
        }

        # --- Step 2: Write audit log FIRST in its own commit so it always persists ---
        log_audit(
            actor_admin_id=g.current_admin.admin_id,
            action_type="concern_delete",
            reason_code=reason_code,
            reason_text=reason_text,
            target_concern_id=concern_id,
            old_value=old_value_snapshot,
        )
        db.session.commit()   # <-- audit row persisted independently

        # --- Step 3: Now apply the soft-delete ---
        concern.is_deleted          = True
        concern.deleted_at          = datetime.now(timezone.utc)
        concern.deleted_by_admin_id = g.current_admin.admin_id
        concern.deleted_reason_code = reason_code
        concern.deleted_reason_text = reason_text
        db.session.commit()

        return jsonify({"message": "Concern deleted successfully"})

    except Exception as e:
        db.session.rollback()
        logger.exception("Error deleting concern %s", concern_id)
        return jsonify({"error": "Internal server error"}), 500