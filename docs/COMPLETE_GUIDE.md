# Vehicle Parking App V2 - Complete Development Guide

## Project Overview

The Vehicle Parking App V2 is a comprehensive multi-user parking management system built with modern web technologies. It provides a complete solution for parking lot management, user reservations, real-time availability tracking, and administrative controls.

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT-based authentication
- **Caching**: Redis for performance optimization
- **Background Jobs**: Celery + Redis for async tasks
- **API Design**: RESTful APIs with proper error handling

### Frontend (Vue.js)
- **Framework**: Vue.js 3 with Composition API
- **State Management**: Vuex for centralized state
- **Routing**: Vue Router with guards
- **UI Framework**: Bootstrap 5 for responsive design
- **HTTP Client**: Axios for API communication

### Background Services
- **Celery Worker**: Handles async tasks
- **Celery Beat**: Scheduled tasks (daily reminders, monthly reports)
- **Redis**: Message broker and caching layer

## 📁 Project Structure

```
mad2project/
├── backend/                 # Flask backend
│   ├── app/                # Application factory
│   ├── models/             # Database models
│   ├── api/                # API blueprints
│   ├── tasks/              # Celery tasks
│   ├── config/             # Configuration files
│   ├── requirements.txt    # Python dependencies
│   ├── init_db.py         # Database initialization
│   └── run.py             # Application entry point
├── frontend/               # Vue.js frontend
│   ├── src/               # Source code
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── store/         # Vuex store
│   │   ├── services/      # API services
│   │   └── router/        # Route definitions
│   ├── public/            # Static files
│   ├── package.json       # Node dependencies
│   └── vue.config.js      # Vue CLI configuration
├── docs/                  # Documentation
├── start.sh              # Development startup script
├── stop.sh               # Service stop script
└── README.md             # Project overview
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **Node.js 16+**
   ```bash
   node --version
   npm --version
   ```

3. **Redis Server** (Optional but recommended)
   ```bash
   # macOS
   brew install redis
   
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # Windows
   # Download from https://redis.io/download
   ```

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mad2project
   ```

2. **Run the setup script**
   ```bash
   ./start.sh
   ```

   This script will:
   - Check dependencies
   - Set up Python virtual environment
   - Install backend dependencies
   - Install frontend dependencies
   - Initialize the database
   - Start all services

3. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000
   - Redis: localhost:6379

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   python init_db.py --init
   python run.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run serve
   ```

3. **Redis Setup**
   ```bash
   redis-server
   ```

4. **Celery Setup**
   ```bash
   cd backend
   source venv/bin/activate
   celery -A app.celery worker --loglevel=info
   celery -A app.celery beat --loglevel=info
   ```

## 🔐 Authentication & Users

### Demo Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Access: Full system administration

**Regular Users:**
- Username: `john_doe`, Password: `password123`
- Username: `jane_smith`, Password: `password123`
- Username: `bob_wilson`, Password: `password123`

### User Roles

1. **Admin (Superuser)**
   - Manage parking lots and spots
   - View all users and reservations
   - Access analytics and reports
   - System configuration

2. **User (Customer)**
   - Register and manage profile
   - Search and reserve parking spots
   - Track reservation history
   - Export personal data

## 🎯 Core Features

### ✅ Milestone 1: Database Models & Schema
- User, Admin, ParkingLot, ParkingSpot, Reservation models
- Proper relationships and constraints
- Programmatic database creation

### ✅ Milestone 2: Authentication & RBAC
- JWT-based authentication
- Role-based access control
- Secure password handling
- Session management

### ✅ Milestone 3: Admin Dashboard
- Parking lot CRUD operations
- Automatic spot creation
- User management
- System statistics

### ✅ Milestone 4: User Dashboard
- Available parking lot browsing
- Auto-allocation reservations
- Park/release functionality
- Reservation tracking

### ✅ Milestone 5: Reservation System
- Complete reservation lifecycle
- Cost calculation based on time
- Historical tracking
- Status management

### ✅ Milestone 6: Analytics & Charts
- Dashboard statistics
- Revenue tracking
- Usage patterns
- Visual charts integration

### ✅ Milestone 7: Redis Caching
- API response caching
- Performance optimization
- Cache expiry policies
- Redis-based storage

### ✅ Milestone 8: Background Jobs
- Daily reminder emails
- Monthly activity reports
- CSV export functionality
- Celery task scheduling

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login` - User/Admin login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Token refresh
- `GET /api/auth/me` - Current user info
- `POST /api/auth/change-password` - Password change

### User APIs
- `GET /api/user/dashboard` - User dashboard data
- `GET /api/user/profile` - User profile
- `PUT /api/user/profile` - Update profile
- `GET /api/user/parking-lots` - Available parking lots
- `POST /api/user/reservations` - Create reservation
- `GET /api/user/reservations` - Reservation history
- `POST /api/user/reservations/{id}/park` - Mark as parked
- `POST /api/user/reservations/{id}/release` - Release parking

### Admin APIs
- `GET /api/admin/dashboard` - Admin dashboard
- `GET /api/admin/users` - All users
- `GET /api/admin/parking-lots` - All parking lots
- `POST /api/admin/parking-lots` - Create parking lot
- `PUT /api/admin/parking-lots/{id}` - Update parking lot
- `DELETE /api/admin/parking-lots/{id}` - Delete parking lot
- `GET /api/admin/parking-lots/{id}/spots` - Lot spots
- `GET /api/admin/reservations` - All reservations

### Analytics APIs
- `GET /api/analytics/dashboard` - Analytics data
- `GET /api/analytics/lots/{id}/analytics` - Lot analytics
- `GET /api/analytics/export/user-data` - Export user data

### Public APIs
- `GET /api/parking/lots` - Public parking lots
- `GET /api/parking/availability` - Real-time availability
- `GET /api/parking/search` - Search parking lots

## 🗄️ Database Schema

### Users Table
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- first_name, last_name
- phone_number
- is_active
- created_at, updated_at
```

### Admins Table
```sql
- id (Primary Key)
- username (Unique, default: 'admin')
- email (Unique)
- password_hash
- first_name, last_name
- is_active
- created_at, updated_at
```

### Parking Lots Table
```sql
- id (Primary Key)
- prime_location_name
- address
- pin_code
- number_of_spots
- price_per_hour
- description
- is_active
- created_at, updated_at
```

### Parking Spots Table
```sql
- id (Primary Key)
- lot_id (Foreign Key -> parking_lots.id)
- spot_number
- status ('A' = Available, 'O' = Occupied)
- is_active
- created_at, updated_at
```

### Reservations Table
```sql
- id (Primary Key)
- user_id (Foreign Key -> users.id)
- spot_id (Foreign Key -> parking_spots.id)
- parking_timestamp
- leaving_timestamp
- reservation_timestamp
- parking_cost
- status ('reserved', 'active', 'completed', 'cancelled')
- vehicle_number
- remarks
- created_at, updated_at
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=jwt-secret-key

# Database
DATABASE_URL=sqlite:///parking_app.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@parkingapp.com
ADMIN_PASSWORD=admin123
```

## 🚀 Deployment

### Development
Use the provided scripts:
```bash
./start.sh  # Start all services
./stop.sh   # Stop all services
```

### Production

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:pass@host:port/db
   ```

2. **Database Migration**
   ```bash
   python init_db.py --init
   ```

3. **Service Management**
   ```bash
   # Use production WSGI server
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   
   # Use process manager for Celery
   celery -A app.celery worker -D
   celery -A app.celery beat -D
   ```

4. **Frontend Build**
   ```bash
   cd frontend
   npm run build
   # Serve dist/ folder with nginx or similar
   ```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm run test:unit
```

### API Testing
Use tools like Postman or curl to test API endpoints:

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123", "user_type": "admin"}'

# Get dashboard (with token)
curl -X GET http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :5000  # Backend
   lsof -i :8080  # Frontend
   lsof -i :6379  # Redis
   
   # Kill the process
   kill -9 PID
   ```

2. **Database Issues**
   ```bash
   # Reset database
   cd backend
   python init_db.py --reset
   ```

3. **Redis Connection Issues**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Start Redis
   redis-server
   ```

4. **Python Virtual Environment**
   ```bash
   # Recreate virtual environment
   rm -rf backend/venv
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Node.js Dependencies**
   ```bash
   # Clear npm cache and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### Debug Mode

Enable debug logging:
```bash
export FLASK_DEBUG=True
export FLASK_ENV=development
```

Check logs:
- Backend: Terminal output
- Frontend: Browser console
- Celery: Terminal output
- Redis: `redis-cli monitor`

## 📊 Performance Optimization

### Backend Optimizations
- Redis caching for frequently accessed data
- Database query optimization
- Pagination for large datasets
- Background job processing

### Frontend Optimizations
- Component lazy loading
- API response caching
- Optimized bundle size
- Progressive loading

### Database Optimizations
- Proper indexing
- Connection pooling
- Query optimization
- Regular maintenance

## 🔒 Security

### Implemented Security Measures
- JWT token authentication
- Password hashing (bcrypt)
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CORS configuration
- Input validation
- Role-based access control

### Security Best Practices
- Regular dependency updates
- Environment variable security
- HTTPS in production
- Rate limiting
- Audit logging
- Secure headers

## 📈 Monitoring & Analytics

### Application Monitoring
- Error tracking
- Performance monitoring
- User activity tracking
- System health checks

### Business Analytics
- Parking utilization rates
- Revenue tracking
- User behavior analysis
- Popular parking locations

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Code Standards
- Python: PEP 8
- JavaScript: ESLint
- Vue.js: Vue style guide
- Git: Conventional commits

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙋 Support

For support and questions:
- Check documentation
- Review troubleshooting guide
- Create GitHub issue
- Contact development team

---

**Happy Parking! 🚗**
