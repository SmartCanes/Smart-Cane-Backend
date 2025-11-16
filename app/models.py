from app import db
from datetime import datetime
import bcrypt

class VIP(db.Model):
    __tablename__ = 'vip_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    vip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vip_name = db.Column(db.String(255), nullable=False)
    vip_image_url = db.Column(db.String(500))
    province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    barangay = db.Column(db.String(100))
    street_address = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    guardians = db.relationship('Guardian', backref='vip', lazy=True)
    locations = db.relationship('GPSLocation', backref='vip', lazy=True)
    reminders = db.relationship('NoteReminder', backref='vip', lazy=True)
    alerts = db.relationship('EmergencyAlert', backref='vip', lazy=True)

class Guardian(db.Model):
    __tablename__ = 'guardian_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    guardian_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    guardian_name = db.Column(db.String(255), nullable=False)
    guardian_image_url = db.Column(db.String(500))
    email = db.Column(db.String(255), nullable=False, unique=True)
    contact_number = db.Column(db.String(20))
    relationship_to_vip = db.Column(db.String(100))
    province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    barangay = db.Column(db.String(100))
    street_address = db.Column(db.Text)
    vip_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.vip_tbl.vip_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
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
    location = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
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

class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alert_tbl'
    __table_args__ = {'schema': 'smart_cane_db'}
    
    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vip_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.vip_tbl.vip_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('smart_cane_db.gps_location_tbl.location_id'), nullable=False)
    triggered_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)