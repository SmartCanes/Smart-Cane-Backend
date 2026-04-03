"""
seed_emergency_logs.py
─────────────────────
Run from your project root:

    python seed_emergency_logs.py

Targets your existing paired devices:
  SC-136901 (device_id=1, vip_id=1)
  SC-136902 (device_id=2, vip_id=2)
  SC-136903 (device_id=3, no VIP)
  SC-136904 (device_id=4, vip_id=3)

SC-136905 is skipped — it is not paired.
"""

import sys
import os
import random
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Device, DeviceLog

# ─────────────────────────────────────────────────────────────────────────────
#  Your existing paired device serials
# ─────────────────────────────────────────────────────────────────────────────

TARGET_SERIALS = [
    "SC-136901",
    "SC-136902",
    "SC-136903",
    "SC-136904",
]

# ─────────────────────────────────────────────────────────────────────────────
#  Fake data pools
# ─────────────────────────────────────────────────────────────────────────────

FAKE_LOCATIONS = [
    "Brgy. San Francisco, Novaliches, Quezon City",
    "Brgy. Talipapa, Novaliches, Quezon City",
    "Brgy. Bagbag, Novaliches, Quezon City",
    "Brgy. Sta. Monica, Novaliches, Quezon City",
    "Brgy. Pasong Putik Proper, Quezon City",
    "Brgy. Greater Lagro, Quezon City",
    "Brgy. Fairview, Quezon City",
    "Brgy. Sauyo, Quezon City",
    "Brgy. Gulod, Novaliches, Quezon City",
    "Brgy. Kaligayahan, Quezon City",
]

# All 6 emergency/fall variants your system actually stores
EMERGENCY_EVENTS = [
    {
        "activity_type": "EMERGENCY",
        "status": "triggered",
        "message": "SOS button was pressed. Immediate assistance required.",
    },
    {
        "activity_type": "SOS",
        "status": "triggered",
        "message": "SOS alert triggered from iCane device.",
    },
    {
        "activity_type": "FALL",
        "status": "triggered",
        "message": "Fall detected by accelerometer sensor.",
    },
    {
        "activity_type": "FALL_DETECTED",
        "status": "triggered",
        "message": "Sudden impact detected. Possible fall event.",
    },
    {
        "activity_type": "LIVE_EMERGENCY",
        "status": "triggered",
        "message": "Emergency alert received via live WebSocket stream.",
    },
    {
        "activity_type": "LIVE_FALL",
        "status": "triggered",
        "message": "Live fall detection triggered from hardware sensor.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def random_past_dt(days_back=30):
    """Random UTC datetime within the last N days."""
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return datetime.now(timezone.utc) - delta


def make_metadata(location: str) -> dict:
    """
    Build a metadata_json blob that matches what the hardware WebSocket
    sends via pushRealtimeAlertLog() in useStore.js.
    The _extract_location() function in emergency.py reads from payload.location.
    """
    lat = round(14.6 + random.uniform(0.05, 0.15), 6)
    lng = round(121.0 + random.uniform(0.02, 0.08), 6)
    return {
        "payload": {
            "lat": lat,
            "lng": lng,
            "location": location,
            "locationLabel": location,
            "source": random.choice(["gps", "mobile"]),
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Seed
# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = create_app()
    with app.app_context():
        print("\n══════════════════════════════════════════")
        print("  iCane Emergency Logs — Seed Script")
        print("══════════════════════════════════════════\n")

        # ── Fetch your existing devices ───────────────────────────────────────
        devices = (
            Device.query
            .filter(Device.device_serial_number.in_(TARGET_SERIALS))
            .all()
        )

        if not devices:
            print("  ✘  None of the target devices were found in the database.")
            print(f"     Expected serials: {TARGET_SERIALS}")
            print("     Make sure you're pointing at the right database.\n")
            sys.exit(1)

        print(f"  ✔  Found {len(devices)} device(s):\n")
        for d in devices:
            vip_label = (
                f"{d.vip.first_name} {d.vip.last_name}" if d.vip else "No VIP"
            )
            guardian_count = len(d.guardian_links)
            print(
                f"     • {d.device_serial_number:<14} "
                f"VIP: {vip_label:<22} "
                f"Guardians: {guardian_count}"
            )

        # ── Insert logs ───────────────────────────────────────────────────────
        num_logs = 12
        print(f"\n  Inserting {num_logs} dummy emergency log(s)...\n")

        inserted = 0
        for i in range(num_logs):
            device   = devices[i % len(devices)]
            event    = EMERGENCY_EVENTS[i % len(EMERGENCY_EVENTS)]
            location = random.choice(FAKE_LOCATIONS)
            created  = random_past_dt(days_back=30)

            # Use the first guardian linked to the device if one exists
            guardian_id = None
            if device.guardian_links:
                guardian_id = random.choice(device.guardian_links).guardian_id

            log = DeviceLog(
                device_id=device.device_id,
                guardian_id=guardian_id,
                activity_type=event["activity_type"],
                status=event["status"],
                message=event["message"],
                metadata_json=make_metadata(location),
                created_at=created,
            )
            db.session.add(log)
            inserted += 1

            print(
                f"  [{i+1:2d}] {event['activity_type']:<18} "
                f"→ {device.device_serial_number}   "
                f"{location[:45]}"
            )

        db.session.commit()

        print(f"\n  ✔  {inserted} log(s) committed successfully.")
        print("\n══════════════════════════════════════════")
        print("  Done! Check your Emergency Logs page.")
        print("══════════════════════════════════════════\n")


if __name__ == "__main__":
    main()