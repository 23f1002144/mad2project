#!/usr/bin/env python3

from models import *
from datetime import datetime, timedelta

# Initialize the database connection
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_system.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    # Get existing reservation
    reservation = Reservation.query.first()
    if reservation:
        print("Current reservation details:")
        print(f"ID: {reservation.id}")
        print(f"Status: {reservation.status}")
        print(f"Parking timestamp: {reservation.parking_timestamp}")
        print(f"Leaving timestamp: {reservation.leaving_timestamp}")
        print(f"Current cost: ${reservation.parking_cost}")
        print(f"Duration hours (method): {reservation.get_duration_hours()}")

        # Get the parking lot price
        spot = ParkingSpot.query.get(reservation.spot_id)
        if spot:
            lot = spot.parking_lot
            print(f"Parking lot: {lot.prime_location_name}")
            print(f"Price per hour: ${lot.price_per_hour}")

            # Test cost calculation
            if reservation.parking_timestamp and reservation.leaving_timestamp:
                calculated_cost = reservation.calculate_cost()
                print(f"Calculated cost: ${calculated_cost}")
            else:
                print("\nNo timestamps set - simulating parking flow:")

                # Simulate parking start
                start_time = datetime.utcnow() - timedelta(hours=2, minutes=30)
                end_time = datetime.utcnow()

                duration_hours = (end_time - start_time).total_seconds() / 3600
                expected_cost = round(duration_hours * lot.price_per_hour, 2)

                print(f"If parked for 2.5 hours at ${lot.price_per_hour}/hour:")
                print(f"Expected cost: ${expected_cost}")
                print(f"Duration: {duration_hours} hours")

                print("\nTesting cost calculation method:")
                # Temporarily set timestamps to test calculation
                old_parking_ts = reservation.parking_timestamp
                old_leaving_ts = reservation.leaving_timestamp

                reservation.parking_timestamp = start_time
                reservation.leaving_timestamp = end_time

                method_cost = reservation.calculate_cost()
                method_duration = reservation.get_duration_hours()

                print(f"Method calculated cost: ${method_cost}")
                print(f"Method calculated duration: {method_duration} hours")
                print(f"Expected cost: ${expected_cost}")
                print(f"Expected duration: {duration_hours} hours")

                # Check if they match
                if abs(method_cost - expected_cost) < 0.01:
                    print("✅ Cost calculation is CORRECT")
                else:
                    print("❌ Cost calculation is INCORRECT")

                if abs(method_duration - duration_hours) < 0.01:
                    print("✅ Duration calculation is CORRECT")
                else:
                    print("❌ Duration calculation is INCORRECT")

                # Restore original values
                reservation.parking_timestamp = old_parking_ts
                reservation.leaving_timestamp = old_leaving_ts
    else:
        print("No reservations found")

    # Test with different scenarios
    print("\n" + "=" * 50)
    print("TESTING VARIOUS SCENARIOS")
    print("=" * 50)

    # Get a parking lot
    lot = ParkingLot.query.first()
    if lot:
        print(
            f"Using parking lot: {lot.prime_location_name} (${lot.price_per_hour}/hour)"
        )

        test_scenarios = [
            (1.0, "1 hour"),
            (2.5, "2.5 hours"),
            (0.5, "30 minutes"),
            (24.0, "24 hours"),
            (0.25, "15 minutes"),
        ]

        for hours, description in test_scenarios:
            start = datetime.utcnow()
            end = start + timedelta(hours=hours)

            # Create a mock reservation for testing
            mock_reservation = Reservation()
            mock_reservation.parking_timestamp = start
            mock_reservation.leaving_timestamp = end

            # Mock the parking_spot relationship
            class MockSpot:
                def __init__(self, lot):
                    self.parking_lot = lot

            mock_reservation.parking_spot = MockSpot(lot)

            calculated_cost = mock_reservation.calculate_cost()
            calculated_duration = mock_reservation.get_duration_hours()
            expected_cost = round(hours * lot.price_per_hour, 2)

            print(
                f"{description}: Duration={calculated_duration}h, Cost=${calculated_cost}, Expected=${expected_cost}"
            )

            if abs(calculated_cost - expected_cost) < 0.01:
                print("  ✅ CORRECT")
            else:
                print("  ❌ INCORRECT")
