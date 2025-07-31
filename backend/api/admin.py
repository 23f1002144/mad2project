from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin authentication"""
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user or current_user.get('type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard():
    """Get admin dashboard data"""
    try:
        # Get statistics
        total_users = User.query.count()
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        available_spots = ParkingSpot.query.filter_by(status='A').count()
        total_reservations = Reservation.query.count()
        active_reservations = Reservation.query.filter_by(status='active').count()
        
        # Get recent reservations
        recent_reservations = Reservation.query.order_by(Reservation.created_at.desc()).limit(10).all()
        
        return jsonify({
            'statistics': {
                'total_users': total_users,
                'total_lots': total_lots,
                'total_spots': total_spots,
                'occupied_spots': occupied_spots,
                'available_spots': available_spots,
                'total_reservations': total_reservations,
                'active_reservations': active_reservations
            },
            'recent_reservations': [r.to_dict() for r in recent_reservations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Get all registered users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_lots():
    """Get all parking lots"""
    try:
        lots = ParkingLot.query.all()
        return jsonify({
            'parking_lots': [lot.to_dict() for lot in lots]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parking-lots', methods=['POST'])
@jwt_required()
@admin_required
def create_parking_lot():
    """Create a new parking lot"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['prime_location_name', 'address', 'pin_code', 'number_of_spots', 'price_per_hour']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create parking lot
        lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            address=data['address'],
            pin_code=data['pin_code'],
            number_of_spots=data['number_of_spots'],
            price_per_hour=data['price_per_hour'],
            description=data.get('description', '')
        )
        
        db.session.add(lot)
        db.session.flush()  # To get the lot ID
        
        # Create parking spots automatically
        for i in range(1, data['number_of_spots'] + 1):
            spot = ParkingSpot(
                lot_id=lot.id,
                spot_number=f"SPOT-{i:03d}",
                status='A'  # Available
            )
            db.session.add(spot)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Parking lot created successfully',
            'parking_lot': lot.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_parking_lot(lot_id):
    """Update a parking lot"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        data = request.get_json()
        
        # Update basic fields
        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.address = data.get('address', lot.address)
        lot.pin_code = data.get('pin_code', lot.pin_code)
        lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
        lot.description = data.get('description', lot.description)
        lot.updated_at = datetime.utcnow()
        
        # Handle number of spots change
        new_spots_count = data.get('number_of_spots')
        if new_spots_count and new_spots_count != lot.number_of_spots:
            current_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
            
            if new_spots_count > current_spots:
                # Add new spots
                for i in range(current_spots + 1, new_spots_count + 1):
                    spot = ParkingSpot(
                        lot_id=lot.id,
                        spot_number=f"SPOT-{i:03d}",
                        status='A'
                    )
                    db.session.add(spot)
            elif new_spots_count < current_spots:
                # Remove spots (only if they're available)
                spots_to_remove = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='A'
                ).order_by(ParkingSpot.id.desc()).limit(current_spots - new_spots_count).all()
                
                if len(spots_to_remove) < (current_spots - new_spots_count):
                    return jsonify({
                        'error': 'Cannot reduce spots. Some spots are currently occupied.'
                    }), 400
                
                for spot in spots_to_remove:
                    db.session.delete(spot)
            
            lot.number_of_spots = new_spots_count
        
        db.session.commit()
        
        return jsonify({
            'message': 'Parking lot updated successfully',
            'parking_lot': lot.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_parking_lot(lot_id):
    """Delete a parking lot (only if all spots are empty)"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        
        # Check if any spots are occupied
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
        if occupied_spots > 0:
            return jsonify({
                'error': 'Cannot delete parking lot. Some spots are currently occupied.'
            }), 400
        
        # Delete all spots and reservations
        ParkingSpot.query.filter_by(lot_id=lot_id).delete()
        db.session.delete(lot)
        db.session.commit()
        
        return jsonify({'message': 'Parking lot deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parking-lots/<int:lot_id>/spots', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_spots(lot_id):
    """Get all spots for a specific parking lot"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
        
        # Get current reservations for occupied spots
        spots_data = []
        for spot in spots:
            spot_dict = spot.to_dict()
            if spot.status == 'O':
                current_reservation = Reservation.query.filter_by(
                    spot_id=spot.id, status='active'
                ).first()
                if current_reservation:
                    spot_dict['current_reservation'] = current_reservation.to_dict()
            spots_data.append(spot_dict)
        
        return jsonify({
            'parking_lot': lot.to_dict(),
            'spots': spots_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reservations', methods=['GET'])
@jwt_required()
@admin_required
def get_all_reservations():
    """Get all reservations with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Reservation.query
        if status:
            query = query.filter_by(status=status)
        
        reservations = query.order_by(Reservation.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reservations': [r.to_dict() for r in reservations.items],
            'total': reservations.total,
            'pages': reservations.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
