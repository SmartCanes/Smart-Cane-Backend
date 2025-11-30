from app import create_app, db
from app.models import Device

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    
    device = Device(
        device_serial_number='SC-136902',
    )
    db.session.add(device)
    db.session.commit()
    print(f"Device created with ID: {device.device_id}")