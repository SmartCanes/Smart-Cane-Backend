from app import create_app, db
from app.models import VIP, Guardian, GPSLocation, NoteReminder, EmergencyAlert

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    
    sample_vip = VIP(
        vip_name="John Doe",
        province="Sample Province",
        city="Sample City",
        barangay="Sample Barangay",
        street_address="123 Sample Street"
    )
    db.session.add(sample_vip)
    db.session.commit()
    print(f"Sample VIP created with ID: {sample_vip.vip_id}")