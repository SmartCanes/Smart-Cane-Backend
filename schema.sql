-- =========================
-- SMART CANE DB (MySQL)
-- matches model.py
-- =========================

SET FOREIGN_KEY_CHECKS = 0;

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
    has_seen_tour TINYINT(1) DEFAULT 0,
    visited_tour_pages JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- login_attempts_tbl (LoginAttempt)
-- =========================
CREATE TABLE login_attempts_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_login_username_created_at (username, created_at),
    INDEX idx_login_ip_created_at (ip_address, created_at)
) ENGINE=InnoDB;

-- =========================
-- otp_tbl (OTP)
-- =========================
CREATE TABLE otp_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(255) NOT NULL,
    is_used TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    used_at TIMESTAMP NULL DEFAULT NULL,
    purpose VARCHAR(50) DEFAULT 'general',

    INDEX idx_otp_email (email)
) ENGINE=InnoDB;

-- =========================
-- device_tbl (Device)
-- =========================
CREATE TABLE device_tbl (
    device_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT NULL,
    device_serial_number VARCHAR(100) NOT NULL UNIQUE,

    is_paired TINYINT(1) DEFAULT 0,
    paired_at TIMESTAMP NULL,
    last_active_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

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
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_gps_vip
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
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
-- note_reminder_tbl (NoteReminder)
-- =========================
CREATE TABLE note_reminder_tbl (
    note_reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT NOT NULL,
    vip_id INT NOT NULL,
    message TEXT NOT NULL,
    reminder_time TIME NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

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
    accepted_at TIMESTAMP NULL,

    INDEX idx_invite_token (token),

    CONSTRAINT fk_invite_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_invite_guardian
        FOREIGN KEY (invited_by_guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- device_config_tbl (DeviceConfig)
-- =========================
CREATE TABLE device_config_tbl (
    config_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL UNIQUE,
    config_json JSON NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_device_config_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- account_history_tbl (AccountHistory)
-- =========================
CREATE TABLE account_history_tbl (
    history_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    guardian_id INT NOT NULL,
    device_id INT NULL,

    action VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_history_guardian_created (guardian_id, created_at),
    INDEX idx_history_device_created (device_id, created_at),

    CONSTRAINT fk_history_guardian
        FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_history_device
        FOREIGN KEY (device_id) REFERENCES device_tbl(device_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;