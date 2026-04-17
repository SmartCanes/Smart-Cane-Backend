-- =========================
-- SMART CANE DB (MySQL)
-- canonical schema (merged from db(1), db(2), and current models)
-- =========================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS reason_catalog_tbl;
DROP TABLE IF EXISTS admin_audit_log_tbl;
DROP TABLE IF EXISTS notification_reads_tbl;
DROP TABLE IF EXISTS notifications_tbl;
DROP TABLE IF EXISTS guardian_concerns_tbl;
DROP TABLE IF EXISTS push_subscription_tbl;
DROP TABLE IF EXISTS device_logs_tbl;
DROP TABLE IF EXISTS device_route_tbl;
DROP TABLE IF EXISTS device_last_location_tbl;
DROP TABLE IF EXISTS account_history_tbl;
DROP TABLE IF EXISTS device_config_tbl;
DROP TABLE IF EXISTS guardian_invitations;
DROP TABLE IF EXISTS emergency_alert_tbl;
DROP TABLE IF EXISTS note_reminder_tbl;
DROP TABLE IF EXISTS gps_location_tbl;
DROP TABLE IF EXISTS device_guardian_tbl;
DROP TABLE IF EXISTS device_tbl;
DROP TABLE IF EXISTS otp_tbl;
DROP TABLE IF EXISTS login_attempts_tbl;
DROP TABLE IF EXISTS admin_archive_tbl;
DROP TABLE IF EXISTS admin_tbl;
DROP TABLE IF EXISTS guardian_tbl;
DROP TABLE IF EXISTS vip_tbl;

SET FOREIGN_KEY_CHECKS = 1;

CREATE DATABASE IF NOT EXISTS smart_cane_db;
USE smart_cane_db;

-- =========================
-- vip_tbl (VIP)
-- =========================
CREATE TABLE vip_tbl (
    vip_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    middle_name VARCHAR(255) NULL,
    last_name VARCHAR(255),
    vip_image_url VARCHAR(500),
    province VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    street_address TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- guardian_tbl (Guardian)
-- =========================
CREATE TABLE guardian_tbl (
    guardian_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    middle_name VARCHAR(255) NULL,
    last_name VARCHAR(255),
    guardian_image_url VARCHAR(500),
    email VARCHAR(255) NOT NULL UNIQUE,
    contact_number VARCHAR(20),
    province VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    village VARCHAR(100),
    street_address TEXT,
    role VARCHAR(50) DEFAULT 'guardian',
    has_seen_tour TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- admin_tbl (Admin)
-- =========================
CREATE TABLE admin_tbl (
    admin_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NULL,
    province VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    barangay VARCHAR(100) NULL,
    street_address TEXT NULL,
    role ENUM('super_admin', 'admin') NOT NULL DEFAULT 'admin',
    is_first_login TINYINT(1) NOT NULL DEFAULT 1,
    profile_image_url VARCHAR(500) NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- login_attempts_tbl (LoginAttempt)
-- =========================
CREATE TABLE login_attempts_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Optional indexes for login throttling / audit lookups
CREATE INDEX idx_login_username_created_at
    ON login_attempts_tbl (username, created_at);

CREATE INDEX idx_login_ip_created_at
    ON login_attempts_tbl (ip_address, created_at);

-- =========================
-- otp_tbl (OTP)
-- =========================
CREATE TABLE otp_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(255) NOT NULL,
    is_used TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    used_at TIMESTAMP NULL DEFAULT NULL,
    purpose VARCHAR(50) DEFAULT 'general'
) ENGINE=InnoDB;

CREATE INDEX idx_otp_email
    ON otp_tbl (email);

-- =========================
-- device_tbl (Device)
-- =========================
CREATE TABLE device_tbl (
    device_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT NULL,
    device_serial_number VARCHAR(100) NOT NULL UNIQUE,
    is_paired TINYINT(1) DEFAULT 0,
    paired_at TIMESTAMP NULL DEFAULT NULL,
    last_active_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_device_vip
        FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- device_guardian_tbl (DeviceGuardian)
-- =========================
CREATE TABLE device_guardian_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    device_name VARCHAR(255) NULL,
    relationship VARCHAR(100) NULL,
    is_emergency_contact TINYINT(1) DEFAULT 0,
    role ENUM('primary', 'secondary', 'guardian') NOT NULL DEFAULT 'guardian',
    guardian_id INT NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT _device_guardian_uc UNIQUE (device_id, guardian_id),

    CONSTRAINT fk_device_guardian_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_device_guardian_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- gps_location_tbl (GPSLocation)
-- =========================
CREATE TABLE gps_location_tbl (
    location_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    location TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_gps_vip
        FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- note_reminder_tbl (NoteReminder)
-- =========================
CREATE TABLE note_reminder_tbl (
    note_reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT NOT NULL,
    vip_id INT NOT NULL,
    message TEXT NOT NULL,
    reminder_time TIME NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_note_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_note_vip
        FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- emergency_alert_tbl (EmergencyAlert)
-- =========================
CREATE TABLE emergency_alert_tbl (
    alert_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT NOT NULL,
    location_id INT NOT NULL,
    triggered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    acknowledged TINYINT(1) DEFAULT 0,

    CONSTRAINT fk_alert_vip
        FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_alert_location
        FOREIGN KEY (location_id) REFERENCES gps_location_tbl(location_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- guardian_invitations (GuardianInvitation)
-- =========================
CREATE TABLE guardian_invitations (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    device_id INT NOT NULL,
    invited_by_guardian_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'expired', 'revoked') NOT NULL DEFAULT 'pending',
    expires_at DATETIME NOT NULL,
    accepted_at TIMESTAMP NULL DEFAULT NULL,

    CONSTRAINT fk_invite_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_invite_guardian
        FOREIGN KEY (invited_by_guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_invite_token
    ON guardian_invitations (token);

-- =========================
-- device_config_tbl (DeviceConfig)
-- =========================
CREATE TABLE device_config_tbl (
    config_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL UNIQUE,
    config_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_device_config_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- device_last_location_tbl (DeviceLastLocation)
-- =========================
CREATE TABLE device_last_location_tbl (
    device_id INT NOT NULL PRIMARY KEY,
    lat DECIMAL(10,7) NULL,
    lng DECIMAL(10,7) NULL,
    sats INT NULL,
    fix_status SMALLINT NOT NULL DEFAULT 0,
    hdop DECIMAL(6,2) NULL,
    gps_status INT NOT NULL DEFAULT 0,
    recorded_at DATETIME NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_device_last_location_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- device_route_tbl (DeviceRoute)
-- =========================
CREATE TABLE device_route_tbl (
    route_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL UNIQUE,
    guardian_id INT NULL,
    destination_label VARCHAR(255) NULL,
    destination_lat DECIMAL(10,7) NOT NULL,
    destination_lng DECIMAL(10,7) NOT NULL,
    route_geojson JSON NULL,
    provider_payload JSON NULL,
    status ENUM('pending', 'active', 'completed', 'cleared', 'failed') NOT NULL DEFAULT 'pending',
    distance_meters DECIMAL(12,2) NULL,
    duration_ms BIGINT NULL,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL DEFAULT NULL,
    cleared_at TIMESTAMP NULL DEFAULT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_route_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_route_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_route_status_updated
    ON device_route_tbl (status, updated_at);

-- =========================
-- account_history_tbl (AccountHistory)
-- =========================
CREATE TABLE account_history_tbl (
    history_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT NOT NULL,
    device_id INT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_history_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_history_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_history_guardian_created
    ON account_history_tbl (guardian_id, created_at);

CREATE INDEX idx_history_device_created
    ON account_history_tbl (device_id, created_at);

-- =========================
-- device_logs_tbl (DeviceLog)
-- =========================
CREATE TABLE device_logs_tbl (
    log_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    guardian_id INT NULL,
    activity_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NULL,
    message TEXT NOT NULL,
    metadata_json JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_device_logs_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_device_logs_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_device_logs_device_id
    ON device_logs_tbl (device_id);

CREATE INDEX idx_device_logs_guardian_id
    ON device_logs_tbl (guardian_id);

CREATE INDEX idx_device_logs_created_at
    ON device_logs_tbl (created_at);

-- =========================
-- push_subscription_tbl (PushSubscription)
-- =========================
CREATE TABLE push_subscription_tbl (
    subscription_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT NOT NULL,
    endpoint TEXT NOT NULL,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_push_subscription_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_push_subscription_guardian
    ON push_subscription_tbl (guardian_id);

-- =========================
-- guardian_concerns_tbl (GuardianConcern)
-- =========================
CREATE TABLE guardian_concerns_tbl (
    concern_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('unread', 'read', 'resolved') NOT NULL DEFAULT 'unread',
    admin_reply TEXT NULL,
    replied_by_admin_id INT NULL,
    replied_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    deleted_by_admin_id INT NULL,
    deleted_reason_code VARCHAR(50) NULL,
    deleted_reason_text VARCHAR(500) NULL,

    CONSTRAINT fk_concern_replied_by_admin
        FOREIGN KEY (replied_by_admin_id) REFERENCES admin_tbl(admin_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_concern_deleted_by_admin
        FOREIGN KEY (deleted_by_admin_id) REFERENCES admin_tbl(admin_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_guardian_concerns_email
    ON guardian_concerns_tbl (email);

CREATE INDEX idx_guardian_concerns_status
    ON guardian_concerns_tbl (status);

CREATE INDEX idx_guardian_concerns_created
    ON guardian_concerns_tbl (created_at);

CREATE INDEX idx_guardian_concerns_deleted
    ON guardian_concerns_tbl (is_deleted);

-- =========================
-- notifications_tbl (Notification)
-- =========================
CREATE TABLE notifications_tbl (
    notification_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    audience ENUM('all_admins', 'super_admins') NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NULL,
    link_path VARCHAR(255) NULL,
    related_concern_id INT NULL,
    related_admin_id INT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE INDEX idx_notifications_audience
    ON notifications_tbl (audience);

CREATE INDEX idx_notifications_type
    ON notifications_tbl (type);

CREATE INDEX idx_notifications_related_concern
    ON notifications_tbl (related_concern_id);

CREATE INDEX idx_notifications_related_admin
    ON notifications_tbl (related_admin_id);

CREATE INDEX idx_notifications_created
    ON notifications_tbl (created_at);

-- =========================
-- notification_reads_tbl (NotificationRead)
-- =========================
CREATE TABLE notification_reads_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    notification_id INT NOT NULL,
    admin_id INT NOT NULL,
    read_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_notification_read_notification_admin
        UNIQUE (notification_id, admin_id),

    CONSTRAINT fk_notification_reads_notification
        FOREIGN KEY (notification_id) REFERENCES notifications_tbl(notification_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_notification_reads_admin
        FOREIGN KEY (admin_id) REFERENCES admin_tbl(admin_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_notification_reads_notification
    ON notification_reads_tbl (notification_id);

CREATE INDEX idx_notification_reads_admin
    ON notification_reads_tbl (admin_id);

CREATE INDEX idx_notification_reads_read_at
    ON notification_reads_tbl (read_at);

-- =========================
-- admin_archive_tbl (AdminArchive)
-- =========================
CREATE TABLE admin_archive_tbl (
    archive_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NULL,
    province VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    barangay VARCHAR(100) NULL,
    street_address TEXT NULL,
    role VARCHAR(50) NOT NULL,
    profile_image_url VARCHAR(500) NULL,
    original_created_at TIMESTAMP NULL DEFAULT NULL,
    archived_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived_by INT NULL,
    archived_reason_code VARCHAR(50) NULL,
    archived_reason_text VARCHAR(500) NULL
) ENGINE=InnoDB;

-- =========================
-- admin_audit_log_tbl (AdminAuditLog)
-- =========================
CREATE TABLE admin_audit_log_tbl (
    audit_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    actor_admin_id INT NOT NULL,
    target_admin_id INT NULL,
    target_concern_id INT NULL,
    action_type VARCHAR(50) NOT NULL,
    old_value_json TEXT NULL,
    new_value_json TEXT NULL,
    reason_code VARCHAR(50) NOT NULL,
    reason_text VARCHAR(500) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'success',
    failure_message VARCHAR(255) NULL,
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_actor_admin
        FOREIGN KEY (actor_admin_id) REFERENCES admin_tbl(admin_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_audit_target_admin
        FOREIGN KEY (target_admin_id) REFERENCES admin_tbl(admin_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_audit_target_concern
        FOREIGN KEY (target_concern_id) REFERENCES guardian_concerns_tbl(concern_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_audit_actor_created
    ON admin_audit_log_tbl (actor_admin_id, created_at);

CREATE INDEX idx_audit_target_admin
    ON admin_audit_log_tbl (target_admin_id);

CREATE INDEX idx_audit_target_concern
    ON admin_audit_log_tbl (target_concern_id);

CREATE INDEX idx_audit_action_created
    ON admin_audit_log_tbl (action_type, created_at);

-- =========================
-- reason_catalog_tbl (optional reason dictionary)
-- =========================
CREATE TABLE reason_catalog_tbl (
    reason_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    reason_code VARCHAR(50) NOT NULL,
    reason_label VARCHAR(120) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,

    CONSTRAINT uq_reason_action_code
        UNIQUE (action_type, reason_code)
) ENGINE=InnoDB;

INSERT IGNORE INTO reason_catalog_tbl (action_type, reason_code, reason_label) VALUES
('admin_delete', 'policy_violation', 'Policy Violation'),
('admin_delete', 'duplicate_account', 'Duplicate Account'),
('admin_delete', 'security_incident', 'Security Incident'),
('admin_delete', 'resigned', 'Resigned'),
('admin_delete', 'inactive', 'Inactive Account'),
('admin_delete', 'other', 'Other'),
('concern_delete', 'spam', 'Spam'),
('concern_delete', 'abusive_content', 'Abusive Content'),
('concern_delete', 'duplicate_concern', 'Duplicate Concern'),
('concern_delete', 'pii_exposure', 'Contains Sensitive PII'),
('concern_delete', 'legal_request', 'Legal/Compliance Request'),
('concern_delete', 'other', 'Other'),
('role_change', 'least_privilege', 'Least Privilege Enforcement'),
('role_change', 'policy_violation', 'Policy Violation'),
('role_change', 'security_incident', 'Security Incident'),
('role_change', 'assignment_change', 'Assignment/Org Change'),
('role_change', 'user_request', 'User Request'),
('role_change', 'other', 'Other'),
('device_delete', 'duplicate_device', 'Duplicate Device'),
('device_delete', 'provisioning_error', 'Provisioning Error'),
('device_delete', 'hardware_replacement', 'Hardware Replacement'),
('device_delete', 'inventory_cleanup', 'Inventory Cleanup'),
('device_delete', 'other', 'Other');

CREATE TABLE guardian_settings_tbl (
    settings_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT NOT NULL,

    allow_location TINYINT(1) NOT NULL DEFAULT 1,
    push_notifications TINYINT(1) NOT NULL DEFAULT 1,
    email_notifications TINYINT(1) NOT NULL DEFAULT 1,
    sms_alerts TINYINT(1) NOT NULL DEFAULT 0,
    two_factor_enabled TINYINT(1) NOT NULL DEFAULT 0,

    updated_at TIMESTAMP NOT NULL 
        DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT uq_guardian_settings_guardian
        UNIQUE (guardian_id),

    CONSTRAINT fk_guardian_settings_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;