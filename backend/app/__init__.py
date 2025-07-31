import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail

from models import db, Admin
from config import config

# from config.celery_config import make_celery

# Initialize extensions
jwt = JWTManager()
cache = Cache()
mail = Mail()


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)

    # Enable CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Register blueprints
    register_blueprints(app)

    # Create tables and default admin
    with app.app_context():
        db.create_all()
        create_default_admin(app)

    # Error handlers
    register_error_handlers(app)

    return app


def register_blueprints(app):
    """Register all blueprints"""
    from api.auth import auth_bp
    from api.admin import admin_bp
    from api.user import user_bp
    from api.parking import parking_bp
    from api.analytics import analytics_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(parking_bp, url_prefix="/api/parking")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden"}), 403


def create_default_admin(app):
    """Create default admin user if it doesn't exist"""
    try:
        admin = Admin.query.filter_by(username=app.config["ADMIN_USERNAME"]).first()
        if not admin:
            admin = Admin(
                username=app.config["ADMIN_USERNAME"],
                email=app.config["ADMIN_EMAIL"],
                first_name=app.config["ADMIN_FIRST_NAME"],
                last_name=app.config["ADMIN_LAST_NAME"],
            )
            admin.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(admin)
            db.session.commit()
            print(f"Default admin created: {admin.username}")
    except Exception as e:
        print(f"Error creating default admin: {e}")
        db.session.rollback()


# Create app instance
app = create_app()

# Create Celery instance
# celery = make_celery(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
