import os
from dotenv import load_dotenv
from app import create_app
from flask_cors import CORS  

# Load environment variables
load_dotenv()

app = create_app()



if __name__ == '__main__':
    ssl_cert = os.getenv("PUBLIC_CERTIFICATE_KEY")
    ssl_key = os.getenv("PRIVATE_CERTIFICATE_KEY")

    ssl_context = None
    if ssl_cert and ssl_key:
        ssl_context = (ssl_cert, ssl_key)

  
    app.run(
        host="0.0.0.0",         
        port=5000,
        ssl_context=ssl_context 
    )