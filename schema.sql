-- =========================
-- SMART CANE DB (MySQL)
-- matches latest model.py
-- =========================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS device_logs_tbl;
DROP TABLE IF EXISTS device_route_tbl;
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