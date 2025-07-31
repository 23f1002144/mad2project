#!/usr/bin/env python3
"""
Test user authentication
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User, Admin
from app import create_app


def test_login():
    """Test user login functionality"""
    app = create_app()

    with app.app_context():
        print("Testing user authentication...")

        # Test john_doe
        user = User.query.filter_by(username="john_doe").first()
        if user:
            print(f"Found user: {user.username}")
            print(f"User active: {user.is_active}")
            print(f"Testing password 'user123'...")
            password_check = user.check_password("user123")
            print(f"Password check result: {password_check}")

            if password_check:
                print("✅ Authentication successful!")
            else:
                print("❌ Authentication failed!")

                # Try checking password hash directly
                from werkzeug.security import check_password_hash

                direct_check = check_password_hash(user.password_hash, "user123")
                print(f"Direct hash check: {direct_check}")
        else:
            print("❌ User not found!")

        # Test admin
        admin = Admin.query.filter_by(username="admin").first()
        if admin:
            print(f"\nFound admin: {admin.username}")
            print(f"Admin active: {admin.is_active}")
            print(f"Testing password 'admin123'...")
            admin_password_check = admin.check_password("admin123")
            print(f"Admin password check result: {admin_password_check}")


if __name__ == "__main__":
    test_login()
