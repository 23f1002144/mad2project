from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models import db, User, Admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint for both users and admin"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type', 'user')  # 'user' or 'admin'
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        if user_type == 'admin':
            # Admin login
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                access_token = create_access_token(
                    identity={'id': admin.id, 'username': admin.username, 'type': 'admin'}
                )
                refresh_token = create_refresh_token(
                    identity={'id': admin.id, 'username': admin.username, 'type': 'admin'}
                )
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': admin.to_dict(),
                    'user_type': 'admin'
                }), 200
        else:
            # User login
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password) and user.is_active:
                access_token = create_access_token(
                    identity={'id': user.id, 'username': user.username, 'type': 'user'}
                )
                refresh_token = create_refresh_token(
                    identity={'id': user.id, 'username': user.username, 'type': 'user'}
                )
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user.to_dict(),
                    'user_type': 'user'
                }), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data.get('phone_number')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(
            identity={'id': user.id, 'username': user.username, 'type': 'user'}
        )
        refresh_token = create_refresh_token(
            identity={'id': user.id, 'username': user.username, 'type': 'user'}
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'user_type': 'user'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh token endpoint"""
    try:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return jsonify({'access_token': new_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['id']
        user_type = current_user['type']
        
        if user_type == 'admin':
            admin = Admin.query.get(user_id)
            if admin:
                return jsonify({
                    'user': admin.to_dict(),
                    'user_type': 'admin'
                }), 200
        else:
            user = User.query.get(user_id)
            if user:
                return jsonify({
                    'user': user.to_dict(),
                    'user_type': 'user'
                }), 200
        
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': 'Old password and new password are required'}), 400
        
        user_id = current_user['id']
        user_type = current_user['type']
        
        if user_type == 'admin':
            admin = Admin.query.get(user_id)
            if admin and admin.check_password(old_password):
                admin.set_password(new_password)
                db.session.commit()
                return jsonify({'message': 'Password changed successfully'}), 200
        else:
            user = User.query.get(user_id)
            if user and user.check_password(old_password):
                user.set_password(new_password)
                db.session.commit()
                return jsonify({'message': 'Password changed successfully'}), 200
        
        return jsonify({'error': 'Invalid old password'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
