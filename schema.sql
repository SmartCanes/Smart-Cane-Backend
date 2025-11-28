        SET FOREIGN_KEY_CHECKS = 0;

        DROP TABLE IF EXISTS device_guardian;
        DROP TABLE IF EXISTS guardian_vip;
        DROP TABLE IF EXISTS emergency_alert_tbl;
        DROP TABLE IF EXISTS note_reminder_tbl;
        DROP TABLE IF EXISTS gps_location_tbl;
        DROP TABLE IF EXISTS device_tbl;
        DROP TABLE IF EXISTS otp_tbl;

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
            email VARCHAR(255),
            contact_number VARCHAR(20),
            relationship_to_vip VARCHAR(100),
            city VARCHAR(100),
            barangay VARCHAR(100),
            province VARCHAR(100),
            street_address TEXT,
            role enum("primary_guardian", "secondary_guardian", "guardian") DEFAULT "guardian",
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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

        CREATE TABLE otp_tbl (
        id int NOT NULL AUTO_INCREMENT,
        email varchar(255) NOT NULL,
        otp_code varchar(6) NOT NULL,
        is_used tinyint(1) DEFAULT '0',
        created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expires_at datetime NOT NULL,
        used_at timestamp DEFAULT NULL,
        PRIMARY KEY (id)
        );


        CREATE TABLE device_tbl (
            device_id INT(11) NOT NULL AUTO_INCREMENT,
            vip_id INT(11) NOT NULL,
            device_serial_number VARCHAR(100) UNIQUE NOT NULL,
            PRIMARY KEY (device_id),
            FOREIGN KEY (vip_id) REFERENCES vip_tbl(vip_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );

        CREATE TABLE device_guardian_tbl (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id INT NOT NULL,
            guardian_id INT NOT NULL,
            FOREIGN KEY (device_id) REFERENCES device_tbl(device_id) ON DELETE CASCADE,
            FOREIGN KEY (guardian_id) REFERENCES guardian_tbl(guardian_id) ON DELETE CASCADE,
            UNIQUE (device_id, guardian_id)
        );