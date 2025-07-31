from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from models import db, User, Reservation, ParkingLot
from flask_mail import Message
from flask import current_app
import requests
import csv
import io
import os


def make_celery(app):
    """Create Celery instance"""
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Celery beat schedule
celery_beat_schedule = {
    "daily-reminder": {
        "task": "tasks.daily_reminder",
        "schedule": crontab(hour=18, minute=0),  # 6 PM daily
    },
    "monthly-report": {
        "task": "tasks.monthly_report",
        "schedule": crontab(
            hour=9, minute=0, day_of_month=1
        ),  # 9 AM on 1st of every month
    },
}


def send_email(to_email, subject, body, html_body=None):
    """Send email using Flask-Mail"""
    try:
        from app import mail

        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body,
            html=html_body,
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_google_chat_notification(message):
    """Send notification via Google Chat webhook"""
    try:
        webhook_url = current_app.config.get("GOOGLE_CHAT_WEBHOOK_URL")
        if not webhook_url:
            return False

        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Google Chat notification: {e}")
        return False


# Celery tasks
def daily_reminder():
    """Send daily reminders to users"""
    try:
        # Get users who haven't made a reservation in the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)

        inactive_users = User.query.filter(
            ~User.id.in_(
                db.session.query(Reservation.user_id)
                .filter(Reservation.created_at >= week_ago)
                .distinct()
            ),
            User.is_active == True,
        ).all()

        # Check if any new parking lots were created
        new_lots = ParkingLot.query.filter(ParkingLot.created_at >= week_ago).all()

        for user in inactive_users:
            # Prepare message
            if new_lots:
                message = f"Hi {user.first_name}! We have new parking lots available. Check them out and book a spot if needed!"
                lots_info = "\n".join(
                    [
                        f"- {lot.prime_location_name} at {lot.address}"
                        for lot in new_lots
                    ]
                )
                message += f"\n\nNew locations:\n{lots_info}"
            else:
                message = f"Hi {user.first_name}! It's been a while since your last parking reservation. Need a spot? Book now!"

            # Send email notification
            email_sent = send_email(
                to_email=user.email,
                subject="Parking Reminder - Book Your Spot!",
                body=message,
            )

            # Send Google Chat notification (if configured)
            chat_sent = send_google_chat_notification(
                f"Daily Reminder sent to {user.username} ({user.email})"
            )

            print(
                f"Reminder sent to {user.username}: Email={email_sent}, Chat={chat_sent}"
            )

        return f"Daily reminders sent to {len(inactive_users)} users"

    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error: {str(e)}"


def monthly_report():
    """Generate and send monthly activity reports"""
    try:
        # Get last month's date range
        today = datetime.utcnow()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)

        # Get all active users
        users = User.query.filter_by(is_active=True).all()

        for user in users:
            # Get user's reservations from last month
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.created_at >= first_day_last_month,
                Reservation.created_at < first_day_this_month,
            ).all()

            if not reservations:
                continue  # Skip users with no activity

            # Calculate statistics
            total_reservations = len(reservations)
            completed_reservations = len(
                [r for r in reservations if r.status == "completed"]
            )
            total_spent = sum(
                [r.parking_cost or 0 for r in reservations if r.status == "completed"]
            )

            # Find most used parking lot
            lot_usage = {}
            for reservation in reservations:
                lot_name = reservation.parking_spot.parking_lot.prime_location_name
                lot_usage[lot_name] = lot_usage.get(lot_name, 0) + 1

            most_used_lot = (
                max(lot_usage.items(), key=lambda x: x[1]) if lot_usage else ("N/A", 0)
            )

            # Calculate total parking duration
            total_duration = sum(
                [
                    r.get_duration_hours()
                    for r in reservations
                    if r.status == "completed"
                    and r.parking_timestamp
                    and r.leaving_timestamp
                ]
            )

            # Generate HTML report
            html_report = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .stat-box {{ 
                        display: inline-block; 
                        margin: 10px; 
                        padding: 15px; 
                        border: 1px solid #ddd; 
                        border-radius: 5px; 
                        text-align: center; 
                        min-width: 150px;
                    }}
                    .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
                    .stat-label {{ font-size: 14px; color: #666; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #f4f4f4; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Monthly Parking Report</h1>
                    <h3>{last_day_last_month.strftime("%B %Y")}</h3>
                    <p>Hello {user.first_name} {user.last_name}!</p>
                </div>
                
                <div class="content">
                    <h2>Your Parking Summary</h2>
                    
                    <div class="stat-box">
                        <div class="stat-number">{total_reservations}</div>
                        <div class="stat-label">Total Reservations</div>
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-number">{completed_reservations}</div>
                        <div class="stat-label">Completed Parkings</div>
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-number">${total_spent:.2f}</div>
                        <div class="stat-label">Total Spent</div>
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-number">{total_duration:.1f}h</div>
                        <div class="stat-label">Total Parking Time</div>
                    </div>
                    
                    <h3>Most Used Parking Lot</h3>
                    <p><strong>{most_used_lot[0]}</strong> ({most_used_lot[1]} times)</p>
                    
                    <h3>Recent Reservations</h3>
                    <table>
                        <tr>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Duration</th>
                            <th>Cost</th>
                            <th>Status</th>
                        </tr>
            """

            for reservation in reservations[:10]:  # Show last 10 reservations
                html_report += f"""
                        <tr>
                            <td>{reservation.created_at.strftime('%Y-%m-%d')}</td>
                            <td>{reservation.parking_spot.parking_lot.prime_location_name}</td>
                            <td>{reservation.get_duration_hours():.1f} hours</td>
                            <td>${reservation.parking_cost or 0:.2f}</td>
                            <td>{reservation.status.title()}</td>
                        </tr>
                """

            html_report += """
                    </table>
                    
                    <p style="margin-top: 30px; font-size: 12px; color: #666;">
                        Thank you for using our parking service!<br>
                        This is an automated report. Please do not reply to this email.
                    </p>
                </div>
            </body>
            </html>
            """

            # Send email
            email_sent = send_email(
                to_email=user.email,
                subject=f"Your Parking Report - {last_day_last_month.strftime('%B %Y')}",
                body=f"Please view this email in HTML format for the best experience.",
                html_body=html_report,
            )

            print(f"Monthly report sent to {user.username}: {email_sent}")

        return f"Monthly reports sent to {len(users)} users"

    except Exception as e:
        print(f"Error in monthly_report task: {e}")
        return f"Error: {str(e)}"


def export_user_data_csv(user_id, email):
    """Export user data to CSV and send via email"""
    try:
        user = User.query.get(user_id)
        if not user:
            return "User not found"

        # Get all user reservations
        reservations = (
            Reservation.query.filter_by(user_id=user_id)
            .order_by(Reservation.created_at.desc())
            .all()
        )

        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(
            [
                "Reservation ID",
                "Parking Lot",
                "Spot Number",
                "Vehicle Number",
                "Reservation Date",
                "Parking Start",
                "Parking End",
                "Duration (Hours)",
                "Cost ($)",
                "Status",
                "Remarks",
            ]
        )

        # Write data
        for reservation in reservations:
            writer.writerow(
                [
                    reservation.id,
                    reservation.parking_spot.parking_lot.prime_location_name,
                    reservation.parking_spot.spot_number,
                    reservation.vehicle_number or "",
                    reservation.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    (
                        reservation.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        if reservation.parking_timestamp
                        else ""
                    ),
                    (
                        reservation.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        if reservation.leaving_timestamp
                        else ""
                    ),
                    reservation.get_duration_hours(),
                    reservation.parking_cost or 0,
                    reservation.status,
                    reservation.remarks or "",
                ]
            )

        csv_content = output.getvalue()
        output.close()

        # Create HTML email with CSV attachment
        html_body = f"""
        <html>
        <body>
            <h2>Your Parking Data Export</h2>
            <p>Hello {user.first_name},</p>
            <p>Your parking data export is ready! The CSV file contains all your parking reservations and details.</p>
            <p>Export generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            <p>Total reservations: {len(reservations)}</p>
            <hr>
            <p style="font-size: 12px; color: #666;">
                This is an automated export. Please save the attached file to your device.
            </p>
        </body>
        </html>
        """

        # For now, we'll send the CSV content in the email body
        # In a production environment, you would attach the CSV file
        plain_body = f"""
Your Parking Data Export

Hello {user.first_name},

Your parking data export is ready! Below is your parking history in CSV format:

{csv_content}

Export generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Total reservations: {len(reservations)}
        """

        # Send email
        email_sent = send_email(
            to_email=email,
            subject="Your Parking Data Export",
            body=plain_body,
            html_body=html_body,
        )

        return f"CSV export sent to {email}: {email_sent}"

    except Exception as e:
        print(f"Error in export_user_data_csv task: {e}")
        return f"Error: {str(e)}"
