import os
from app import create_app
from flask_cors import CORS

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

app = create_app()

if __name__ == "__main__":
    MODE = os.environ.get("MODE", "development") == "development"
    port = int(os.environ.get("PORT", 5001))

    ssl_cert = os.getenv("PUBLIC_CERTIFICATE_KEY") if not MODE else None
    ssl_key = os.getenv("PRIVATE_CERTIFICATE_KEY") if not MODE else None
    ssl_context = (ssl_cert, ssl_key) if ssl_cert and ssl_key else None

    if ssl_context:
        print("Running with HTTPS")
    else:
        print("Running with HTTP")

    app.run(host="0.0.0.0", port=port, ssl_context=ssl_context, debug=MODE)
