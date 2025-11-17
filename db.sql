CREATE DATABASE IF NOT EXISTS smart_cane_db;
USE smart_cane_db;

CREATE TABLE vip_tbl (
    vip_id INT(11) NOT NULL AUTO_INCREMENT,
    vip_name VARCHAR(255) NOT NULL,
    vip_image_url VARCHAR(500),
    province VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    street_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (vip_id)
);

CREATE TABLE guardian_tbl (
    guardian_id INT(11) NOT NULL AUTO_INCREMENT,
    vip_id INT(11) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    guardian_name VARCHAR(255),
    guardian_image_url VARCHAR(500),
    email VARCHAR(255),
    contact_number VARCHAR(20),
    relationship_to_vip VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    province VARCHAR(100),
    street_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guardian_id),
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE gps_location_tbl (
    location_id INT(11) NOT NULL AUTO_INCREMENT,
    vip_id INT(11) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    location TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (location_id),
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE note_reminder_tbl (
    note_reminder_id INT(11) NOT NULL AUTO_INCREMENT,
    guardian_id INT(11) NOT NULL,
    vip_id INT(11) NOT NULL,
    message TEXT,
    reminder_time TIME,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (note_reminder_id),
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE emergency_alert_tbl (
    alert_id INT(11) NOT NULL AUTO_INCREMENT,
    vip_id INT(11) NOT NULL,
    location_id INT(11) NOT NULL,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged TINYINT(1) DEFAULT 0, 
    PRIMARY KEY (alert_id),
    FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES gps_location_tbl(location_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);