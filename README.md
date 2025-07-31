# Vehicle Parking App V2

A multi-user parking management application built with Flask API backend and VueJS frontend.

## Features
- Admin dashboard for managing parking lots and spots
- User registration and parking spot reservation
- Real-time parking status tracking
- Cost calculation and reservation history
- Analytics and charts
- Background jobs for notifications and reports
- Redis caching for performance optimization

## Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: VueJS
- **Database**: SQLite
- **Caching**: Redis
- **Background Jobs**: Celery + Redis
- **Styling**: Bootstrap
- **Authentication**: JWT/Flask-Security

## Project Structure
```
mad2project/
├── backend/
│   ├── app/
│   ├── models/
│   ├── api/
│   ├── tasks/
│   └── config/
├── frontend/
│   ├── src/
│   ├── components/
│   └── views/
└── docs/
```

## Setup Instructions
1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `npm install`
4. Initialize database: `python init_db.py`
5. Start Redis server
6. Start Celery worker and beat
7. Run Flask backend: `python app.py`
8. Run VueJS frontend: `npm run serve`

## Roles
- **Admin**: Superuser with full control over parking lots and spots
- **User**: Can register, login, and reserve parking spots

## Core Functionalities
- Parking lot and spot management
- User reservation system
- Real-time status tracking
- Cost calculation
- Analytics and reporting
- Background notifications
- CSV export functionality
