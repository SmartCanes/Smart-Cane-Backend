import os
from dotenv import load_dotenv
from app import create_app
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = create_app()

if __name__ == "__main__":
    DEV_MODE = os.environ.get("DEV_MODE", "development") == "development"

    ssl_cert = os.getenv("PUBLIC_CERTIFICATE_KEY") if not DEV_MODE else None
    ssl_key = os.getenv("PRIVATE_CERTIFICATE_KEY") if not DEV_MODE else None
    ssl_context = (ssl_cert, ssl_key) if ssl_cert and ssl_key else None

    if ssl_context:
        print("Running with HTTPS")
    else:
        print("Running with HTTP")

    app.run(host="127.0.0.1", port=5000, ssl_context=ssl_context, debug=DEV_MODE)
