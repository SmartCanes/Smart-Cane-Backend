# 🦯 Smart Cane Backend (Flask API)

Backend service for the **Smart Cane / iCane Guardian Platform**, built with **Flask and MySQL**.

This API powers the full system including authentication, device management, GPS tracking, reminders, notifications, and guardian–VIP interactions.

---

## 📌 Overview

This backend handles all core system logic for the Smart Cane ecosystem, including:

- 👤 Guardian authentication & account management
- 📡 Device pairing and relationship mapping
- 🧑 VIP profile management
- 📍 Location tracking and route data
- 🔔 Notifications and emergency alerts
- 📝 Reminders and logs
- 📤 File uploads (profile images, documents)

---

## ⚙️ Tech Stack

- 🐍 Python 3.10+
- 🌶️ Flask
- 🗄️ Flask-SQLAlchemy
- 🔐 Flask-JWT-Extended
- 🚦 Flask-Limiter
- 🌐 Flask-CORS
- 🐬 MySQL (PyMySQL)
- 📧 SMTP Email (OTP & notifications)

---

## 🚀 Setup Guide

### 1. Prerequisites

- Python 3.10+
- MySQL Server
- Database: `smart_cane_db`

---

### 2. Create Virtual Environment

```bash id="venv_setup"
python -m venv .venv
```

Activate:

**Git Bash / Linux / macOS**

```bash id="venv_unix"
source .venv/Scripts/activate
```

**Windows PowerShell**

```powershell id="venv_win"
.venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```bash id="install_deps"
pip install -r requirements.txt
```

---

### 4. Environment Configuration

Create a `.env` file:

```env id="env_config"
MODE=development

DATABASE_URL=mysql+pymysql://root:@localhost:3306/smart_cane_db
JWT_SECRET_KEY=change-this-secret

FRONTEND_URL=http://localhost:3000

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=you@example.com
MAIL_PASSWORD=your-app-password
MAIL_SENDER_NAME=iCane Smart Cane
```

---

### 5. Database Setup

#### Option A (Recommended)

```bash id="db_import"
mysql -u root -p < schema.sql
```

#### Option B (Auto setup + sample data)

```bash id="init_db"
python init_db.py
```

---

### 6. Run the Server

```bash id="run_server"
python run.py
```

API runs at:

```
http://0.0.0.0:5001
```

---

## 📡 API Structure

### 🔐 Auth

```
/api/auth
```

Handles login, OTP, registration, password reset, and session management.

---

### 👤 Guardian

```
/api/guardian
```

Profile management, push subscriptions, history logs.

---

### 📱 Device

```
/api/device
```

Pairing, invites, GPS routes, logs, guardianship roles.

---

### 🧑 VIP

```
/api/vip
```

VIP profile updates and image handling.

---

### ⏰ Reminders

```
/api/reminders
```

CRUD operations for reminders.

---

### 📬 Contact

```
/api/contact
```

Public feedback and concern submissions.

---

## 🧠 Core System Features

### 🔐 Authentication System

- JWT-based authentication (cookie storage)
- OTP verification for secure login/register
- Rate-limited login protection

---

### 📡 Device System

- Device generation & validation
- Guardian-device pairing
- Multi-guardian support per device
- Invite-based access control

---

### 📍 Tracking & Routes

- GPS route storage per device
- Last known location tracking
- Route history retrieval

---

### 🔔 Notifications & Alerts

- Push notification subscription system
- Emergency alert handling
- Real-time guardian updates

---

### 📝 Logs & Audit System

- Action history tracking
- Device event logs
- Admin traceability support

---

### 📧 Email System

- OTP email verification
- Password reset emails
- Guardian invitation emails

---

## 📁 Utility Modules

- **auth.py** → JWT protection decorators
- **responses.py** → Standard API response format
- **serializer.py** → Safe model serialization
- **history_logger.py** → Audit logging system
- **email_service.py** → SMTP OTP & invites

---

## 📦 File Uploads

- Max size: **2MB**
- Allowed types: `png`, `jpg`, `jpeg`, `gif`, `webp`
- Used for:
  - Guardian profiles
  - VIP profiles
  - Documents/images

---

## 🧪 Utility Scripts

```bash id="run_backend"
python run.py
```

```bash id="init_db_script"
python init_db.py
```

```bash id="seed_logs"
python seed_emergency_logs.py
```

---

## ⚠️ Notes

- JWT is stored in cookies (not local storage)
- SMTP is required for OTP + invites
- Some features include fallback behavior if email service is unavailable
- Production requires secure environment variable handling

---

## 📌 Summary

The Smart Cane Backend is a secure, modular Flask API that powers a real-time Smart Cane IoT guardian system with authentication, device tracking, emergency alerts, and communication services.

---
