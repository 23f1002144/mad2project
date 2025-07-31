from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ParkingLot, ParkingSpot, Reservation, User
from datetime import datetime, timedelta
from sqlalchemy import func, desc

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_analytics_dashboard():
    """Get analytics data for dashboard"""
    try:
        current_user = get_jwt_identity()
        user_type = current_user.get('type')
        
        if user_type == 'admin':
            return get_admin_analytics()
        elif user_type == 'user':
            return get_user_analytics(current_user['id'])
        else:
            return jsonify({'error': 'Invalid user type'}), 403
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_admin_analytics():
    """Get analytics data for admin dashboard"""
    try:
        # Time-based statistics
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Basic statistics
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        total_users = User.query.count()
        total_reservations = Reservation.query.count()
        
        # Current occupancy
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        occupancy_rate = round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 2)
        
        # Revenue statistics
        total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            Reservation.status == 'completed'
        ).scalar() or 0
        
        monthly_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            Reservation.status == 'completed',
            Reservation.leaving_timestamp >= month_ago
        ).scalar() or 0
        
        weekly_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            Reservation.status == 'completed',
            Reservation.leaving_timestamp >= week_ago
        ).scalar() or 0
        
        # Popular parking lots
        popular_lots = db.session.query(
            ParkingLot.id,
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('reservation_count')
        ).join(ParkingSpot).join(Reservation).group_by(
            ParkingLot.id, ParkingLot.prime_location_name
        ).order_by(desc('reservation_count')).limit(5).all()
        
        # Daily reservation trends (last 7 days)
        daily_reservations = []
        for i in range(7):
            date = today - timedelta(days=i)
            count = Reservation.query.filter(
                func.date(Reservation.created_at) == date
            ).count()
            daily_reservations.append({
                'date': date.isoformat(),
                'reservations': count
            })
        
        # Hourly distribution of reservations today
        hourly_data = []
        for hour in range(24):
            count = Reservation.query.filter(
                func.date(Reservation.created_at) == today,
                func.extract('hour', Reservation.created_at) == hour
            ).count()
            hourly_data.append({
                'hour': hour,
                'reservations': count
            })
        
        # Parking duration analysis
        avg_duration = db.session.query(
            func.avg(
                func.julianday(Reservation.leaving_timestamp) - 
                func.julianday(Reservation.parking_timestamp)
            ) * 24
        ).filter(
            Reservation.status == 'completed',
            Reservation.parking_timestamp.isnot(None),
            Reservation.leaving_timestamp.isnot(None)
        ).scalar() or 0
        
        return jsonify({
            'overview': {
                'total_lots': total_lots,
                'total_spots': total_spots,
                'total_users': total_users,
                'total_reservations': total_reservations,
                'occupied_spots': occupied_spots,
                'occupancy_rate': occupancy_rate,
                'avg_parking_duration_hours': round(avg_duration, 2)
            },
            'revenue': {
                'total_revenue': round(total_revenue, 2),
                'monthly_revenue': round(monthly_revenue, 2),
                'weekly_revenue': round(weekly_revenue, 2)
            },
            'popular_lots': [
                {
                    'lot_id': lot.id,
                    'name': lot.prime_location_name,
                    'reservation_count': lot.reservation_count
                } for lot in popular_lots
            ],
            'trends': {
                'daily_reservations': daily_reservations,
                'hourly_distribution': hourly_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_analytics(user_id):
    """Get analytics data for user dashboard"""
    try:
        # User's reservation statistics
        total_reservations = Reservation.query.filter_by(user_id=user_id).count()
        completed_reservations = Reservation.query.filter_by(user_id=user_id, status='completed').count()
        
        # Total spent
        total_spent = db.session.query(func.sum(Reservation.parking_cost)).filter_by(
            user_id=user_id, status='completed'
        ).scalar() or 0
        
        # Average parking duration
        avg_duration = db.session.query(
            func.avg(
                func.julianday(Reservation.leaving_timestamp) - 
                func.julianday(Reservation.parking_timestamp)
            ) * 24
        ).filter_by(
            user_id=user_id, status='completed'
        ).filter(
            Reservation.parking_timestamp.isnot(None),
            Reservation.leaving_timestamp.isnot(None)
        ).scalar() or 0
        
        # Most used parking lots
        favorite_lots = db.session.query(
            ParkingLot.id,
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('usage_count')
        ).join(ParkingSpot).join(Reservation).filter(
            Reservation.user_id == user_id
        ).group_by(
            ParkingLot.id, ParkingLot.prime_location_name
        ).order_by(desc('usage_count')).limit(3).all()
        
        # Monthly spending (last 6 months)
        monthly_spending = []
        for i in range(6):
            start_date = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
            end_date = start_date.replace(month=start_date.month % 12 + 1, day=1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1, day=1)
            
            spent = db.session.query(func.sum(Reservation.parking_cost)).filter(
                Reservation.user_id == user_id,
                Reservation.status == 'completed',
                Reservation.leaving_timestamp >= start_date,
                Reservation.leaving_timestamp < end_date
            ).scalar() or 0
            
            monthly_spending.append({
                'month': start_date.strftime('%Y-%m'),
                'amount': round(spent, 2)
            })
        
        # Recent reservations
        recent_reservations = Reservation.query.filter_by(user_id=user_id).order_by(
            Reservation.created_at.desc()
        ).limit(5).all()
        
        return jsonify({
            'overview': {
                'total_reservations': total_reservations,
                'completed_reservations': completed_reservations,
                'total_spent': round(total_spent, 2),
                'avg_parking_duration_hours': round(avg_duration, 2)
            },
            'favorite_lots': [
                {
                    'lot_id': lot.id,
                    'name': lot.prime_location_name,
                    'usage_count': lot.usage_count
                } for lot in favorite_lots
            ],
            'monthly_spending': monthly_spending,
            'recent_activity': [r.to_dict() for r in recent_reservations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/lots/<int:lot_id>/analytics', methods=['GET'])
@jwt_required()
def get_lot_analytics(lot_id):
    """Get detailed analytics for a specific parking lot"""
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        lot = ParkingLot.query.get_or_404(lot_id)
        
        # Basic statistics
        total_spots = ParkingSpot.query.filter_by(lot_id=lot_id).count()
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
        
        # Revenue for this lot
        total_revenue = db.session.query(func.sum(Reservation.parking_cost)).join(
            ParkingSpot
        ).filter(
            ParkingSpot.lot_id == lot_id,
            Reservation.status == 'completed'
        ).scalar() or 0
        
        # Total reservations
        total_reservations = db.session.query(func.count(Reservation.id)).join(
            ParkingSpot
        ).filter(ParkingSpot.lot_id == lot_id).scalar() or 0
        
        # Average duration
        avg_duration = db.session.query(
            func.avg(
                func.julianday(Reservation.leaving_timestamp) - 
                func.julianday(Reservation.parking_timestamp)
            ) * 24
        ).join(ParkingSpot).filter(
            ParkingSpot.lot_id == lot_id,
            Reservation.status == 'completed',
            Reservation.parking_timestamp.isnot(None),
            Reservation.leaving_timestamp.isnot(None)
        ).scalar() or 0
        
        # Peak hours analysis
        peak_hours = []
        for hour in range(24):
            count = db.session.query(func.count(Reservation.id)).join(
                ParkingSpot
            ).filter(
                ParkingSpot.lot_id == lot_id,
                func.extract('hour', Reservation.parking_timestamp) == hour
            ).scalar() or 0
            peak_hours.append({
                'hour': hour,
                'reservations': count
            })
        
        return jsonify({
            'lot_info': lot.to_dict(),
            'statistics': {
                'total_spots': total_spots,
                'occupied_spots': occupied_spots,
                'occupancy_rate': round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 2),
                'total_revenue': round(total_revenue, 2),
                'total_reservations': total_reservations,
                'avg_duration_hours': round(avg_duration, 2)
            },
            'peak_hours': peak_hours
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/export/user-data', methods=['GET'])
@jwt_required()
def export_user_data():
    """Export user's parking data for CSV download"""
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') != 'user':
            return jsonify({'error': 'User access required'}), 403
        
        user_id = current_user['id']
        
        # Get all user reservations
        reservations = Reservation.query.filter_by(user_id=user_id).order_by(
            Reservation.created_at.desc()
        ).all()
        
        # Prepare data for CSV export
        export_data = []
        for reservation in reservations:
            export_data.append({
                'reservation_id': reservation.id,
                'parking_lot': reservation.parking_spot.parking_lot.prime_location_name,
                'spot_number': reservation.parking_spot.spot_number,
                'vehicle_number': reservation.vehicle_number,
                'reservation_date': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'parking_start': reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else '',
                'parking_end': reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else '',
                'duration_hours': reservation.get_duration_hours(),
                'cost': reservation.parking_cost,
                'status': reservation.status,
                'remarks': reservation.remarks or ''
            })
        
        return jsonify({'export_data': export_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
