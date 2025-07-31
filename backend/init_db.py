#!/usr/bin/env python3
"""
Database initialization script for Vehicle Parking App V2
This script creates all database tables and sets up initial data.
"""

import os
import sys
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Admin, User, ParkingLot, ParkingSpot, Reservation


def init_database():
    """Initialize database with tables and default data"""
    app = create_app()

    with app.app_context():
        print("Initializing database...")

        # Drop all tables (for fresh start)
        print("Dropping existing tables...")
        db.drop_all()

        # Create all tables
        print("Creating tables...")
        db.create_all()

        # Create default admin
        print("Creating default admin...")
        admin = Admin(
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
            first_name=app.config["ADMIN_FIRST_NAME"],
            last_name=app.config["ADMIN_LAST_NAME"],
        )
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)

        # Create sample users
        print("Creating sample users...")
        sample_users = [
            {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "password": "password123",
            },
            {
                "username": "jane_smith",
                "email": "jane.smith@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "phone_number": "+1234567891",
                "password": "password123",
            },
            {
                "username": "bob_wilson",
                "email": "bob.wilson@example.com",
                "first_name": "Bob",
                "last_name": "Wilson",
                "phone_number": "+1234567892",
                "password": "password123",
            },
        ]

        for user_data in sample_users:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data["phone_number"],
            )
            user.set_password(user_data["password"])
            db.session.add(user)

        # Create sample parking lots
        print("Creating sample parking lots...")
        sample_lots = [
            {
                "prime_location_name": "Downtown Plaza",
                "address": "123 Main Street, Downtown",
                "pin_code": "12345",
                "number_of_spots": 50,
                "price_per_hour": 5.0,
                "description": "Premium parking location in the heart of downtown with 24/7 security.",
            },
            {
                "prime_location_name": "Shopping Mall West",
                "address": "456 Mall Avenue, West Side",
                "pin_code": "12346",
                "number_of_spots": 100,
                "price_per_hour": 3.0,
                "description": "Convenient parking for shopping and entertainment activities.",
            },
            {
                "prime_location_name": "Business District",
                "address": "789 Corporate Blvd, Business District",
                "pin_code": "12347",
                "number_of_spots": 75,
                "price_per_hour": 8.0,
                "description": "Professional parking facility serving the business district.",
            },
            {
                "prime_location_name": "Airport Terminal",
                "address": "321 Airport Road, Terminal Area",
                "pin_code": "12348",
                "number_of_spots": 200,
                "price_per_hour": 12.0,
                "description": "Long-term and short-term parking near the airport terminal.",
            },
            {
                "prime_location_name": "University Campus",
                "address": "654 University Drive, Campus",
                "pin_code": "12349",
                "number_of_spots": 30,
                "price_per_hour": 2.0,
                "description": "Student-friendly parking with affordable rates.",
            },
        ]

        for lot_data in sample_lots:
            lot = ParkingLot(
                prime_location_name=lot_data["prime_location_name"],
                address=lot_data["address"],
                pin_code=lot_data["pin_code"],
                number_of_spots=lot_data["number_of_spots"],
                price_per_hour=lot_data["price_per_hour"],
                description=lot_data["description"],
            )
            db.session.add(lot)
            db.session.flush()  # To get the lot ID

            # Create parking spots for each lot
            print(
                f"Creating {lot_data['number_of_spots']} spots for {lot_data['prime_location_name']}..."
            )
            for i in range(1, lot_data["number_of_spots"] + 1):
                spot = ParkingSpot(
                    lot_id=lot.id, spot_number=f"SPOT-{i:03d}", status="A"  # Available
                )
                db.session.add(spot)

        # Commit all changes
        db.session.commit()

        print("\nDatabase initialization completed successfully!")
        print(
            f"Created admin user: {app.config['ADMIN_USERNAME']} / {app.config['ADMIN_PASSWORD']}"
        )
        print("Created sample users:")
        for user_data in sample_users:
            print(f"  - {user_data['username']} / {user_data['password']}")
        print("Created parking lots:")
        for lot_data in sample_lots:
            print(
                f"  - {lot_data['prime_location_name']} ({lot_data['number_of_spots']} spots)"
            )

        return True


def reset_database():
    """Reset database to initial state"""
    app = create_app()

    with app.app_context():
        print("Resetting database...")

        # Update all spots to available
        spots = ParkingSpot.query.all()
        for spot in spots:
            spot.status = "A"

        # Cancel all active reservations
        active_reservations = Reservation.query.filter_by(status="active").all()
        for reservation in active_reservations:
            reservation.status = "cancelled"
            reservation.updated_at = datetime.utcnow()

        db.session.commit()
        print("Database reset completed!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Database management for Vehicle Parking App"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Reset database to initial state"
    )
    parser.add_argument(
        "--init", action="store_true", help="Initialize database with sample data"
    )

    args = parser.parse_args()

    if args.reset:
        reset_database()
    elif args.init:
        init_database()
    else:
        # Default action is to initialize
        init_database()
