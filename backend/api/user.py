from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

user_bp = Blueprint("user", __name__)


def user_required(f):
    """Decorator to require user authentication"""

    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user or current_user.get("type") != "user":
            return jsonify({"error": "User access required"}), 403
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@user_required
def get_dashboard():
    """Get user dashboard data"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        # Get user's current active reservation
        active_reservation = Reservation.query.filter_by(
            user_id=user_id, status="active"
        ).first()

        # Get user's reservation history
        reservations = (
            Reservation.query.filter_by(user_id=user_id)
            .order_by(Reservation.created_at.desc())
            .limit(10)
            .all()
        )

        # Get user statistics
        total_reservations = Reservation.query.filter_by(user_id=user_id).count()
        total_spent = (
            db.session.query(db.func.sum(Reservation.parking_cost))
            .filter_by(user_id=user_id, status="completed")
            .scalar()
            or 0
        )

        return (
            jsonify(
                {
                    "active_reservation": (
                        active_reservation.to_dict() if active_reservation else None
                    ),
                    "recent_reservations": [r.to_dict() for r in reservations],
                    "statistics": {
                        "total_reservations": total_reservations,
                        "total_spent": round(total_spent, 2),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
@user_required
def get_profile():
    """Get user profile"""
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
@user_required
def update_profile():
    """Update user profile"""
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        # Update allowed fields
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.updated_at = datetime.utcnow()

        db.session.commit()

        return (
            jsonify(
                {"message": "Profile updated successfully", "user": user.to_dict()}
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route("/parking-lots", methods=["GET"])
@jwt_required()
@user_required
def get_available_parking_lots():
    """Get available parking lots"""
    try:
        lots = ParkingLot.query.filter_by(is_active=True).all()

        lots_data = []
        for lot in lots:
            lot_dict = lot.to_dict()
            # Add available spots count
            available_spots = ParkingSpot.query.filter_by(
                lot_id=lot.id, status="A", is_active=True
            ).count()
            lot_dict["available_spots"] = available_spots
            lots_data.append(lot_dict)

        return jsonify({"parking_lots": lots_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/reservations", methods=["POST"])
@jwt_required()
@user_required
def create_reservation():
    """Create a new reservation"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.get_json()

        lot_id = data.get("lot_id")
        vehicle_number = data.get("vehicle_number")

        if not lot_id or not vehicle_number:
            return jsonify({"error": "Lot ID and vehicle number are required"}), 400

        # Check if user already has an active reservation
        existing_reservation = Reservation.query.filter_by(
            user_id=user_id, status="active"
        ).first()
        if existing_reservation:
            return jsonify({"error": "You already have an active reservation"}), 400

        # Find first available spot in the lot
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id, status="A", is_active=True
        ).first()

        if not available_spot:
            return jsonify({"error": "No available spots in this parking lot"}), 400

        # Create reservation
        reservation = Reservation(
            user_id=user_id,
            spot_id=available_spot.id,
            vehicle_number=vehicle_number,
            status="reserved",
            remarks=data.get("remarks", ""),
        )

        # Update spot status
        available_spot.status = "O"  # Occupied
        available_spot.updated_at = datetime.utcnow()

        db.session.add(reservation)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Reservation created successfully",
                    "reservation": reservation.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route("/reservations/<int:reservation_id>/park", methods=["POST"])
@jwt_required()
@user_required
def park_vehicle(reservation_id):
    """Mark vehicle as parked (start parking timer)"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        reservation = Reservation.query.filter_by(
            id=reservation_id, user_id=user_id
        ).first()

        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        if reservation.status != "reserved":
            return jsonify({"error": "Invalid reservation status"}), 400

        # Update reservation
        reservation.parking_timestamp = datetime.utcnow()
        reservation.status = "active"
        reservation.updated_at = datetime.utcnow()

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Vehicle parked successfully",
                    "reservation": reservation.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route("/reservations/<int:reservation_id>/release", methods=["POST"])
@jwt_required()
@user_required
def release_parking_spot(reservation_id):
    """Release parking spot (end parking)"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        reservation = Reservation.query.filter_by(
            id=reservation_id, user_id=user_id
        ).first()

        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        if reservation.status != "active":
            return jsonify({"error": "Invalid reservation status"}), 400

        # Update reservation
        reservation.leaving_timestamp = datetime.utcnow()
        reservation.status = "completed"
        reservation.parking_cost = reservation.calculate_cost()
        reservation.updated_at = datetime.utcnow()

        # Update spot status
        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = "A"  # Available
        spot.updated_at = datetime.utcnow()

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Parking spot released successfully",
                    "reservation": reservation.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route("/reservations", methods=["GET"])
@jwt_required()
@user_required
def get_user_reservations():
    """Get user's reservation history"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        status = request.args.get("status")

        query = Reservation.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)

        reservations = query.order_by(Reservation.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return (
            jsonify(
                {
                    "reservations": [r.to_dict() for r in reservations.items],
                    "total": reservations.total,
                    "pages": reservations.pages,
                    "current_page": page,
                    "per_page": per_page,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/reservations/<int:reservation_id>", methods=["GET"])
@jwt_required()
@user_required
def get_reservation_details(reservation_id):
    """Get specific reservation details"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        reservation = Reservation.query.filter_by(
            id=reservation_id, user_id=user_id
        ).first()

        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        return jsonify({"reservation": reservation.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
