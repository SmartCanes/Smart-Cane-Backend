from app import create_app, db
from app.models import Device

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    

    for i in range(5):
        device = Device(
            device_serial_number=f'SC-13690{i+1}',
        )
        db.session.add(device)
        db.session.commit()
    print(f"Device created with ID: {device.device_id}")