#!/usr/bin/env python3
"""
Simple Flask app runner without Celery
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Import models and blueprints
from models import db
from api.auth import auth_bp
from api.parking import parking_bp


def create_app():
    """Create Flask application without Celery"""
    app = Flask(__name__)

    # Basic configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_system.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your-secret-key-here"

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(parking_bp, url_prefix="/api/parking")

    @app.route("/")
    def index():
        return {"message": "Vehicle Parking Management System API", "status": "running"}

    @app.route("/health")
    def health():
        return {"status": "healthy", "database": "connected"}

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Starting Flask backend server...")
    print("📊 Database: SQLite (parking_system.db)")
    print("🌐 API Base URL: http://localhost:5001")
    print("📋 Available endpoints:")
    print("   POST /api/auth/register - User registration")
    print("   POST /api/auth/login - User/Admin login")
    print("   GET /api/parking/lots - Get parking lots")
    print("   ... and more")

    app.run(debug=True, host="0.0.0.0", port=5001)
