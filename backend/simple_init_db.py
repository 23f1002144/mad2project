#!/usr/bin/env python3
"""
Simple database initialization script without Celery dependencies
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Import models
from models import db, User, Admin, ParkingLot, ParkingSpot, Reservation


def create_app():
    """Create a simple Flask app for database initialization"""
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_system.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your-secret-key-here"

    db.init_app(app)
    return app


def init_database():
    """Initialize the database with tables and demo data"""
    app = create_app()

    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping existing tables...")
        db.drop_all()

        print("Creating tables...")
        db.create_all()

        # Create demo admin
        print("Creating demo admin...")
        admin = Admin(
            username="admin",
            email="admin@parkingapp.com",
            first_name="System",
            last_name="Administrator",
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # Create demo users
        print("Creating demo users...")
        users_data = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "password": "user123",
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "phone_number": "+1234567891",
                "password": "user123",
            },
        ]

        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data["phone_number"],
            )
            user.set_password(user_data["password"])
            db.session.add(user)

        # Create demo parking lots
        print("Creating demo parking lots...")
        lots_data = [
            {
                "prime_location_name": "Downtown Mall Parking",
                "address": "123 Main Street, Downtown City",
                "pin_code": "12345",
                "number_of_spots": 50,
                "price_per_hour": 5.0,
                "description": "Convenient parking near shopping mall and restaurants",
            },
            {
                "prime_location_name": "Airport Terminal Parking",
                "address": "456 Airport Road, City",
                "pin_code": "67890",
                "number_of_spots": 100,
                "price_per_hour": 8.0,
                "description": "Long-term and short-term parking for air travelers",
            },
            {
                "prime_location_name": "Business District Plaza",
                "address": "789 Corporate Blvd, Business District",
                "pin_code": "11111",
                "number_of_spots": 30,
                "price_per_hour": 6.0,
                "description": "Premium parking for business professionals",
            },
        ]

        for lot_data in lots_data:
            lot = ParkingLot(**lot_data)
            db.session.add(lot)

        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")

        # Generate parking spots for each lot
        print("Generating parking spots...")
        lots = ParkingLot.query.all()
        for lot in lots:
            for i in range(1, lot.number_of_spots + 1):
                spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=f"S{i:03d}",  # S001, S002, etc.
                    status="A",  # Available
                )
                db.session.add(spot)

        db.session.commit()
        print(f"Generated parking spots for {len(lots)} lots")

        print("✅ Database initialization completed successfully!")
        print("\nDemo Credentials:")
        print("Admin: username='admin', password='admin123'")
        print("User 1: username='john_doe', password='user123'")
        print("User 2: username='jane_smith', password='user123'")


if __name__ == "__main__":
    init_database()
