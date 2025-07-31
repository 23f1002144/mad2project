#!/usr/bin/env python3
"""
Celery worker script for Vehicle Parking App V2
"""

import os
from app import create_app
from config.celery_config import make_celery

# Create Flask app and Celery instance
app = create_app()
celery = make_celery(app)

# Import tasks to register them
from tasks import daily_reminder, monthly_report, export_user_data_csv

if __name__ == '__main__':
    # Configure Celery beat schedule
    celery.conf.beat_schedule = {
        'daily-reminder': {
            'task': 'tasks.daily_reminder',
            'schedule': 60.0,  # Every 60 seconds for testing (change to crontab for production)
        },
        'monthly-report': {
            'task': 'tasks.monthly_report',
            'schedule': 300.0,  # Every 5 minutes for testing (change to crontab for production)
        },
    }
    
    celery.conf.timezone = 'UTC'
    
    print("Starting Celery worker...")
    print("Available tasks:")
    print("  - daily_reminder")
    print("  - monthly_report") 
    print("  - export_user_data_csv")
    
    # Start the worker
    celery.start()
