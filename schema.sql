SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS device_guardian_tbl;
DROP TABLE IF EXISTS vip_guardian_tbl;
DROP TABLE IF EXISTS emergency_alert_tbl;
DROP TABLE IF EXISTS note_reminder_tbl;
DROP TABLE IF EXISTS gps_location_tbl;
DROP TABLE IF EXISTS device_tbl;
DROP TABLE IF EXISTS otp_tbl;
DROP TABLE IF EXISTS login_attempts_tbl;
DROP TABLE IF EXISTS guardian_tbl;
DROP TABLE IF EXISTS vip_tbl;

SET FOREIGN_KEY_CHECKS = 1;

CREATE DATABASE IF NOT EXISTS smart_cane_db;
USE smart_cane_db;

CREATE TABLE guardian_tbl (
    guardian_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    guardian_name VARCHAR(255),
    guardian_image_url VARCHAR(500),
    email VARCHAR(255) UNIQUE NOT NULL,
    contact_number VARCHAR(20),
    province VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    village VARCHAR(100),
    street_address TEXT,
    role VARCHAR(50) DEFAULT 'guardian',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE vip_tbl (
    vip_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_name VARCHAR(255) NOT NULL,
    vip_image_url VARCHAR(500),
    province VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    street_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE gps_location_tbl (
    location_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT(11) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    location TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE note_reminder_tbl (
    note_reminder_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guardian_id INT(11) NOT NULL,
    vip_id INT(11) NOT NULL,
    message TEXT NOT NULL,
    reminder_time TIME NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE emergency_alert_tbl (
    alert_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT(11) NOT NULL,
    location_id INT(11) NOT NULL,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged TINYINT(1) DEFAULT 0,
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES gps_location_tbl(location_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE otp_tbl (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    is_used TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP DEFAULT NULL,
    INDEX idx_email (email)
);

CREATE TABLE login_attempts_tbl (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username_created_at (username, created_at),
    INDEX idx_ip_created_at (ip_address, created_at)
);

CREATE TABLE device_tbl (
    device_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vip_id INT(11) NULL,
    device_serial_number VARCHAR(100) UNIQUE NOT NULL,
    is_paired BOOLEAN DEFAULT FALSE,
    paired_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE device_guardian_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    guardian_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (device_id, guardian_id),
    FOREIGN KEY (device_id) REFERENCES device_tbl(device_id) ON DELETE CASCADE,
    FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id) ON DELETE CASCADE
);

CREATE TABLE vip_guardian_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vip_id INT NOT NULL,
    guardian_id INT NOT NULL,
    relationship_to_vip VARCHAR(100),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (vip_id, guardian_id),
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id) ON DELETE CASCADE,
    FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id) ON DELETE CASCADE
);
