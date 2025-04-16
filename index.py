# Remember to switch DEBUG to false later in production.

# index.py
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from routes.households import household_bp
from routes.candidates import candidate_bp
from routes.villages import village_bp
from routes.auth import auth_bp
from routes.facial_recognition import facial_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

CORS(app, supports_credentials=True, expose_headers=["Authorization"])

# Register Blueprints
app.register_blueprint(household_bp)
app.register_blueprint(candidate_bp)
app.register_blueprint(village_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(facial_bp)

# Run Server
if __name__ == '__main__':
    api_host = os.getenv('API_HOST', '0.0.0.0')
    api_port = int(os.getenv('API_PORT', 5000))
    app.run(debug=True, host=api_host, port=api_port)