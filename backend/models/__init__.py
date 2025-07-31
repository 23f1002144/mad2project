from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for customers who can reserve parking spots"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Admin(db.Model):
    """Admin model for superuser with full control"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, default='admin')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert admin to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ParkingLot(db.Model):
    """Parking lot model representing physical parking areas"""
    __tablename__ = 'parking_lots'
    
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False, default=0)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')
    
    def get_available_spots_count(self):
        """Get count of available spots"""
        return ParkingSpot.query.filter_by(lot_id=self.id, status='A').count()
    
    def get_occupied_spots_count(self):
        """Get count of occupied spots"""
        return ParkingSpot.query.filter_by(lot_id=self.id, status='O').count()
    
    def to_dict(self):
        """Convert parking lot to dictionary"""
        return {
            'id': self.id,
            'prime_location_name': self.prime_location_name,
            'address': self.address,
            'pin_code': self.pin_code,
            'number_of_spots': self.number_of_spots,
            'price_per_hour': self.price_per_hour,
            'description': self.description,
            'is_active': self.is_active,
            'available_spots': self.get_available_spots_count(),
            'occupied_spots': self.get_occupied_spots_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ParkingSpot(db.Model):
    """Individual parking spot within a parking lot"""
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A-Available, O-Occupied
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='parking_spot', lazy=True, cascade='all, delete-orphan')
    
    # Unique constraint for spot number within a lot
    __table_args__ = (db.UniqueConstraint('lot_id', 'spot_number', name='unique_spot_per_lot'),)
    
    def to_dict(self):
        """Convert parking spot to dictionary"""
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'spot_number': self.spot_number,
            'status': self.status,
            'status_text': 'Available' if self.status == 'A' else 'Occupied',
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Reservation(db.Model):
    """Reservation model linking users to parking spots"""
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=True)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    reservation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parking_cost = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='reserved')  # reserved, active, completed, cancelled
    vehicle_number = db.Column(db.String(20), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_cost(self):
        """Calculate parking cost based on time and lot price"""
        if self.parking_timestamp and self.leaving_timestamp:
            parking_lot = self.parking_spot.parking_lot
            duration_hours = (self.leaving_timestamp - self.parking_timestamp).total_seconds() / 3600
            return round(duration_hours * parking_lot.price_per_hour, 2)
        return 0.0
    
    def get_duration_hours(self):
        """Get parking duration in hours"""
        if self.parking_timestamp and self.leaving_timestamp:
            return round((self.leaving_timestamp - self.parking_timestamp).total_seconds() / 3600, 2)
        elif self.parking_timestamp:
            return round((datetime.utcnow() - self.parking_timestamp).total_seconds() / 3600, 2)
        return 0.0
    
    def to_dict(self):
        """Convert reservation to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'spot_id': self.spot_id,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'reservation_timestamp': self.reservation_timestamp.isoformat() if self.reservation_timestamp else None,
            'parking_cost': self.parking_cost,
            'status': self.status,
            'vehicle_number': self.vehicle_number,
            'remarks': self.remarks,
            'duration_hours': self.get_duration_hours(),
            'parking_lot_name': self.parking_spot.parking_lot.prime_location_name if self.parking_spot else None,
            'spot_number': self.parking_spot.spot_number if self.parking_spot else None,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
