#!/usr/bin/env python3
"""
Main application entry point for Vehicle Parking App V2
"""

import os
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'on']
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("Starting Vehicle Parking App V2...")
    print(f"Debug mode: {debug}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("Swagger UI will be available at: http://localhost:5000/swagger")
    
    app.run(debug=debug, host=host, port=port)
