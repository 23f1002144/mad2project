from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ParkingLot, ParkingSpot, Reservation
from flask_caching import Cache

parking_bp = Blueprint('parking', __name__)

@parking_bp.route('/lots', methods=['GET'])
def get_parking_lots():
    """Get all active parking lots with availability"""
    try:
        lots = ParkingLot.query.filter_by(is_active=True).all()
        
        lots_data = []
        for lot in lots:
            lot_dict = lot.to_dict()
            lots_data.append(lot_dict)
        
        return jsonify({'parking_lots': lots_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>', methods=['GET'])
def get_parking_lot_details(lot_id):
    """Get detailed parking lot information"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        
        # Get spot statistics
        total_spots = ParkingSpot.query.filter_by(lot_id=lot_id, is_active=True).count()
        available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='A', is_active=True).count()
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O', is_active=True).count()
        
        lot_dict = lot.to_dict()
        lot_dict.update({
            'total_spots': total_spots,
            'available_spots': available_spots,
            'occupied_spots': occupied_spots,
            'occupancy_rate': round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 2)
        })
        
        return jsonify({'parking_lot': lot_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
def get_parking_spots(lot_id):
    """Get all spots for a parking lot"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        spots = ParkingSpot.query.filter_by(lot_id=lot_id, is_active=True).all()
        
        return jsonify({
            'parking_lot': lot.to_dict(),
            'spots': [spot.to_dict() for spot in spots]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/availability', methods=['GET'])
def get_availability():
    """Get real-time parking availability across all lots"""
    try:
        # Get availability summary for all lots
        lots = ParkingLot.query.filter_by(is_active=True).all()
        
        availability_data = []
        for lot in lots:
            available_count = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='A', is_active=True
            ).count()
            
            total_count = ParkingSpot.query.filter_by(
                lot_id=lot.id, is_active=True
            ).count()
            
            availability_data.append({
                'lot_id': lot.id,
                'lot_name': lot.prime_location_name,
                'address': lot.address,
                'total_spots': total_count,
                'available_spots': available_count,
                'occupied_spots': total_count - available_count,
                'availability_percentage': round((available_count / total_count * 100) if total_count > 0 else 0, 2),
                'price_per_hour': lot.price_per_hour
            })
        
        return jsonify({'availability': availability_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/search', methods=['GET'])
def search_parking():
    """Search parking lots by location or name"""
    try:
        query = request.args.get('q', '').strip()
        min_spots = request.args.get('min_spots', type=int)
        max_price = request.args.get('max_price', type=float)
        
        # Build query
        lots_query = ParkingLot.query.filter_by(is_active=True)
        
        if query:
            search_filter = db.or_(
                ParkingLot.prime_location_name.ilike(f'%{query}%'),
                ParkingLot.address.ilike(f'%{query}%'),
                ParkingLot.pin_code.ilike(f'%{query}%')
            )
            lots_query = lots_query.filter(search_filter)
        
        if max_price:
            lots_query = lots_query.filter(ParkingLot.price_per_hour <= max_price)
        
        lots = lots_query.all()
        
        # Filter by available spots if specified
        if min_spots:
            filtered_lots = []
            for lot in lots:
                available_count = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='A', is_active=True
                ).count()
                if available_count >= min_spots:
                    filtered_lots.append(lot)
            lots = filtered_lots
        
        # Prepare response data
        results = []
        for lot in lots:
            lot_dict = lot.to_dict()
            available_count = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='A', is_active=True
            ).count()
            lot_dict['available_spots'] = available_count
            results.append(lot_dict)
        
        return jsonify({
            'results': results,
            'total_found': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/reservations/<int:reservation_id>/status', methods=['GET'])
@jwt_required()
def get_reservation_status(reservation_id):
    """Get current status of a reservation"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user has access to this reservation
        if current_user.get('type') == 'user':
            reservation = Reservation.query.filter_by(
                id=reservation_id, user_id=current_user['id']
            ).first()
        else:
            # Admin can view any reservation
            reservation = Reservation.query.get(reservation_id)
        
        if not reservation:
            return jsonify({'error': 'Reservation not found'}), 404
        
        return jsonify({'reservation': reservation.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>/reserve', methods=['POST'])
@jwt_required()
def quick_reserve(lot_id):
    """Quick reservation for first available spot"""
    try:
        current_user = get_jwt_identity()
        
        if current_user.get('type') != 'user':
            return jsonify({'error': 'Only users can make reservations'}), 403
        
        user_id = current_user['id']
        data = request.get_json()
        
        vehicle_number = data.get('vehicle_number')
        if not vehicle_number:
            return jsonify({'error': 'Vehicle number is required'}), 400
        
        # Check if user already has an active reservation
        existing_reservation = Reservation.query.filter_by(
            user_id=user_id, status__in=['reserved', 'active']
        ).first()
        if existing_reservation:
            return jsonify({'error': 'You already have an active reservation'}), 400
        
        # Find first available spot
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id, status='A', is_active=True
        ).first()
        
        if not available_spot:
            return jsonify({'error': 'No available spots in this parking lot'}), 400
        
        # Create reservation
        reservation = Reservation(
            user_id=user_id,
            spot_id=available_spot.id,
            vehicle_number=vehicle_number,
            status='reserved',
            remarks=data.get('remarks', '')
        )
        
        # Update spot status
        available_spot.status = 'O'
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'message': 'Spot reserved successfully',
            'reservation': reservation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
