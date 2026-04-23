import json
import logging
import traceback
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from sqlalchemy import func

from app import db
from app.models import Admin, AdminArchive, AdminAuditLog, Device, GuardianConcern
from app.routes.notifications import create_notification
from app.utils.audit import log_audit

logger = logging.getLogger(__name__)


restore_bp = Blueprint("restore", __name__, url_prefix="/api/admin/audit-logs")

RESTORABLE_ACTIONS = {
	"admin_delete",
	"concern_delete",
	"device_delete",
	"device_deleted",
}
DEVICE_DELETE_ACTIONS = {"device_delete", "device_deleted"}
CONCERN_STATUS_OPTIONS = {"unread", "read", "resolved"}


def require_super_admin():
	claims = get_jwt()
	if claims.get("role") != "super_admin":
		return jsonify({"message": "Access denied. Super admin only."}), 403
	return None


def _safe_parse_json(text_value):
	if not text_value:
		return {}
	try:
		parsed = json.loads(text_value)
		return parsed if isinstance(parsed, dict) else {}
	except Exception:
		return {}


def _default_restore_reason(payload):
	code = str((payload or {}).get("reason_code") or "restore_from_audit").strip() or "restore_from_audit"
	text = str((payload or {}).get("reason_text") or "Restored from audit log entry.").strip()
	if len(text) < 10:
		text = "Restored from audit log entry."
	return code, text


def _log_restore_action(actor_id, action_type, old_payload, new_payload, reason_code, reason_text):
	log_audit(
		actor_admin_id=actor_id,
		action_type=action_type,
		reason_code=reason_code,
		reason_text=reason_text,
		old_value=old_payload,
		new_value=new_payload,
	)


def _restore_deleted_admin(old_payload):
	deleted_admin_id = old_payload.get("deleted_admin_id")
	if not deleted_admin_id:
		return None, "Missing deleted_admin_id in audit payload.", 400

	restored_first_login = bool(
		old_payload.get("was_first_login", old_payload.get("is_first_login", False))
	)

	archive = (
		AdminArchive.query.filter_by(admin_id=int(deleted_admin_id))
		.order_by(AdminArchive.archived_at.desc())
		.first()
	)
	if not archive:
		return None, "No archived admin record found for this audit entry.", 404

	existing_username = Admin.query.filter_by(username=archive.username).first()
	if existing_username:
		# If the conflicting admin IS the same person (already restored), treat as idempotent success.
		if existing_username.admin_id == int(archive.admin_id):
			db.session.delete(archive)  # clean up stale archive row
			return {
				"restored_action_type": "admin_restore",
				"restored_admin_id": existing_username.admin_id,
				"restored_admin_email": existing_username.email,
			}, None, None
		return None, "Cannot restore admin because username already exists.", 409

	archived_email = str(archive.email or old_payload.get("email") or "").strip()
	if not archived_email:
		return None, "Cannot restore admin because archived email is missing.", 400

	existing_email = Admin.query.filter(func.lower(Admin.email) == archived_email.lower()).first()
	if existing_email:
		# If the conflicting admin IS the same person (already restored), treat as idempotent success.
		if existing_email.admin_id == int(archive.admin_id):
			db.session.delete(archive)  # clean up stale archive row
			return {
				"restored_action_type": "admin_restore",
				"restored_admin_id": existing_email.admin_id,
				"restored_admin_email": existing_email.email,
			}, None, None
		return None, "Cannot restore admin because email already exists in active admins.", 409

	restored = Admin(
		admin_id=archive.admin_id,
		username=archive.username,
		email=archived_email,
		password=archive.password,
		first_name=archive.first_name,
		middle_name=archive.middle_name,
		last_name=archive.last_name,
		contact_number=archive.contact_number,
		province=archive.province,
		city=archive.city,
		barangay=archive.barangay,
		street_address=archive.street_address,
		role=archive.role if archive.role in ("admin", "super_admin") else "admin",
		is_first_login=restored_first_login,
		profile_image_url=archive.profile_image_url,
		created_at=archive.original_created_at or datetime.now(timezone.utc),
		updated_at=datetime.now(timezone.utc),
	)
	db.session.add(restored)
	db.session.delete(archive)

	return {
		"restored_action_type": "admin_restore",
		"restored_admin_id": restored.admin_id,
		"restored_admin_email": restored.email,
	}, None, None


def _restore_deleted_concern(old_payload, audit=None):
	# Resolve concern_id: prefer target_concern_id on the audit row, fall back to snapshot.
	concern_id = (
		(audit.target_concern_id if audit else None)
		or old_payload.get("concern_id")
	)
	if not concern_id:
		return None, "Missing concern_id in audit record.", 400

	concern = GuardianConcern.query.get(int(concern_id))
	if not concern:
		return None, "Concern record not found in database.", 404

	# If concern is already active, treat as idempotent success.
	if not concern.is_deleted:
		return {
			"restored_action_type": "concern_restore",
			"restored_concern_id": concern.concern_id,
			"message": "Concern is already active (no changes needed).",
		}, None, None

	# Un-delete the concern — also restore any snapshot fields if they were captured.
	concern.is_deleted          = False
	concern.deleted_at          = None
	concern.deleted_by_admin_id = None
	concern.deleted_reason_code = None
	concern.deleted_reason_text = None

	# Restore the original status from the snapshot if available, else keep current.
	if old_payload.get("status") in CONCERN_STATUS_OPTIONS:
		concern.status = old_payload["status"]

	return {
		"restored_action_type": "concern_restore",
		"restored_concern_id": concern.concern_id,
	}, None, None


def _restore_deleted_device(old_payload):
	serial = str(
		old_payload.get("deleted_device_serial")
		or old_payload.get("device_serial_number")
		or ""
	).strip()
	if not serial:
		return None, "Missing deleted device serial in audit payload.", 400

	# Check if a device with this serial already exists.
	existing = Device.query.filter(func.lower(Device.device_serial_number) == serial.lower()).first()
	if existing:
		# If the original device_id matches (already restored), treat as idempotent success.
		original_device_id = old_payload.get("deleted_device_id")
		if original_device_id and existing.device_id == int(original_device_id):
			return {
				"restored_action_type": "device_restore",
				"restored_device_serial": serial,
				"restored_device_id": existing.device_id,
				"message": "Device already exists (no changes needed).",
			}, None, None
		return (
			None,
			f"Cannot restore: a device with serial number '{serial}' already exists.",
			409,
		)

	# Attempt to restore with original device_id so foreign-key references in audit logs stay intact.
	original_device_id = old_payload.get("deleted_device_id")
	try:
		restored = Device(
			device_serial_number=serial,
			is_paired=bool(old_payload.get("is_paired", False)),
			vip_id=old_payload.get("vip_id"),
		)
		if original_device_id:
			restored.device_id = int(original_device_id)
		db.session.add(restored)
	except Exception:
		# If setting the original PK fails (e.g. auto-increment conflict), insert without it.
		db.session.rollback()
		restored = Device(
			device_serial_number=serial,
			is_paired=bool(old_payload.get("is_paired", False)),
			vip_id=old_payload.get("vip_id"),
		)
		db.session.add(restored)

	return {
		"restored_action_type": "device_restore",
		"restored_device_serial": serial,
	}, None, None


def _notify_restore(actor, action_type, result_payload):
	try:
		actor_name = (
			" ".join(part for part in [actor.first_name, actor.last_name] if part).strip()
			if actor
			else "A super admin"
		) or "A super admin"
		actor_role = ((actor.role if actor and actor.role else "super_admin") or "super_admin").replace("_", " ")

		if action_type == "admin_delete":
			body = (
				f"{actor_name} ({actor_role}) restored admin account "
				f"{result_payload.get('restored_admin_email', '')}."
			)
			link_path = "/admins"
			notif_type = "admin_restored"
			title = "Admin account restored"
		elif action_type == "concern_delete":
			body = (
				f"{actor_name} ({actor_role}) restored guardian concern "
				f"#{result_payload.get('restored_concern_id', '-')}."
			)
			link_path = "/guardian-concerns"
			notif_type = "concern_restored"
			title = "Guardian concern restored"
		elif action_type in DEVICE_DELETE_ACTIONS:
			body = (
				f"{actor_name} ({actor_role}) restored device "
				f"{result_payload.get('restored_device_serial', '-')}."
			)
			link_path = "/devices"
			notif_type = "device_restored"
			title = "Device restored"
		else:
			return

		create_notification(
			audience="all_admins",
			type=notif_type,
			title=title,
			body=body,
			link_path=link_path,
			related_admin_id=actor.admin_id if actor else None,
		)
	except Exception:
		pass


@restore_bp.route("/<int:audit_id>/restore", methods=["POST"])
@jwt_required()
def restore_from_audit(audit_id):
	err = require_super_admin()
	if err:
		return err

	audit = AdminAuditLog.query.get(audit_id)
	if not audit:
		return jsonify({"message": "Audit record not found."}), 404

	if audit.action_type not in RESTORABLE_ACTIONS:
		return jsonify({"message": "This audit action is not restorable."}), 400

	if audit.status not in ("success", "restored"):
		return jsonify({"message": "Only successful delete actions can be restored."}), 400

	old_payload = _safe_parse_json(audit.old_value_json)
	actor_id = int(get_jwt_identity())
	actor = Admin.query.get(actor_id)
	reason_code, reason_text = _default_restore_reason(request.get_json(silent=True) or {})

	try:
		if audit.action_type == "admin_delete":
			result_payload, error_message, error_status = _restore_deleted_admin(old_payload)
		elif audit.action_type == "concern_delete":
			result_payload, error_message, error_status = _restore_deleted_concern(old_payload, audit)
		elif audit.action_type in DEVICE_DELETE_ACTIONS:
			result_payload, error_message, error_status = _restore_deleted_device(old_payload)
		else:
			return jsonify({"message": "This audit action is not restorable."}), 400

		if error_message:
			return jsonify({"message": error_message}), error_status

		# Mark the original delete audit row as "restored".
		audit.status = "restored"

		# Write a new audit entry recording this restore action.
		_log_restore_action(
			actor_id=actor_id,
			action_type=result_payload["restored_action_type"],
			old_payload={"source_audit_id": audit.audit_id, "source_action_type": audit.action_type},
			new_payload=result_payload,
			reason_code=reason_code,
			reason_text=reason_text,
		)

		db.session.commit()
		_notify_restore(actor, audit.action_type, result_payload)

		return jsonify(
			{
				"message": result_payload.get("message") or "Restore completed successfully.",
				**result_payload,
			}
		), 200
	except Exception:
		db.session.rollback()
		logger.exception("restore_from_audit failed for audit_id=%s", audit_id)
		return jsonify({"message": "Failed to restore record. Please try again."}), 500
