import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(
        host="0.0.0.0",         
        port=5000,
        ssl_context=("../server.cert", "../server.key") 
    )