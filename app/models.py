from app import db
from datetime import datetime
import bcrypt
from datetime import datetime
from app import db

class OTP(db.Model):
    __tablename__ = 'otp_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    otp_code = db.Column(db.String(6), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.TIMESTAMP, nullable=True)
    
    def __repr__(self):
        return f'<OTP {self.email}>'

class VIP(db.Model):
    __tablename__ = 'vip_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    vip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.guardian_tbl.guardian_id'), nullable=False)
    vip_name = db.Column(db.String(255), nullable=False)
    vip_image_url = db.Column(db.String(500))
    vip_qr_code = db.Column(db.String(255))
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    barangay = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    guardian = db.relationship('Guardian', backref='vips', lazy=True)
    locations = db.relationship('GPSLocation', backref='vip', lazy=True)
    reminders = db.relationship('NoteReminder', backref='vip', lazy=True)
    alerts = db.relationship('EmergencyAlert', backref='vip', lazy=True)

class Guardian(db.Model):
    __tablename__ = 'guardian_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    guardian_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guardian_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    guardian_image_url = db.Column(db.String(500))
    email = db.Column(db.String(255), nullable=False, unique=True)
    contact_number = db.Column(db.String(20), nullable=False)
    relationship_to_vip = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    barangay = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reminders = db.relationship('NoteReminder', backref='guardian', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
class GPSLocation(db.Model):
    __tablename__ = 'gps_location_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vip_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.vip_tbl.vip_id'), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    location = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    alerts = db.relationship('EmergencyAlert', backref='location', lazy=True)

class NoteReminder(db.Model):
    __tablename__ = 'note_reminder_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    note_reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.guardian_tbl.guardian_id'), nullable=False)
    vip_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.vip_tbl.vip_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alert_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vip_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.vip_tbl.vip_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.gps_location_tbl.location_id'))
    triggered_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('smart_cane_db.guardian_tbl.guardian_id'))
    
    # Relationships
    guardian = db.relationship('Guardian', foreign_keys=[acknowledged_by], backref='acknowledged_alerts', lazy=True)