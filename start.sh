#!/bin/bash

# Vehicle Parking App V2 - Development Startup Script
# This script starts all necessary services for local development

echo "🚗 Starting Vehicle Parking App V2..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

if ! command_exists redis-server; then
    echo -e "${YELLOW}⚠️  Redis is not installed. Please install Redis for caching and background jobs.${NC}"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    echo "   You can continue without Redis, but some features will be disabled."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✅ Dependencies check complete${NC}"

# Setup backend
echo -e "\n${BLUE}Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your configuration${NC}"
fi

# Initialize database
echo "Initializing database..."
python init_db.py --init

echo -e "${GREEN}✅ Backend setup complete${NC}"

# Setup frontend
echo -e "\n${BLUE}Setting up frontend...${NC}"
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✅ Frontend setup complete${NC}"

# Start Redis (if available)
if command_exists redis-server; then
    echo -e "\n${BLUE}Starting Redis...${NC}"
    if ! port_in_use 6379; then
        redis-server --daemonize yes
        echo -e "${GREEN}✅ Redis started on port 6379${NC}"
    else
        echo -e "${YELLOW}⚠️  Redis is already running on port 6379${NC}"
    fi
fi

# Start services
echo -e "\n${BLUE}Starting services...${NC}"

# Function to start backend
start_backend() {
    cd backend
    source venv/bin/activate
    export FLASK_ENV=development
    export FLASK_DEBUG=True
    python run.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    echo -e "${GREEN}✅ Backend started on http://localhost:5000 (PID: $BACKEND_PID)${NC}"
}

# Function to start frontend
start_frontend() {
    cd frontend
    npm run serve &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    echo -e "${GREEN}✅ Frontend started on http://localhost:8080 (PID: $FRONTEND_PID)${NC}"
}

# Function to start Celery worker (if Redis is available)
start_celery() {
    if command_exists redis-server && port_in_use 6379; then
        cd backend
        source venv/bin/activate
        celery -A app.celery worker --loglevel=info &
        CELERY_PID=$!
        echo $CELERY_PID > celery.pid
        echo -e "${GREEN}✅ Celery worker started (PID: $CELERY_PID)${NC}"
        
        # Start Celery beat
        celery -A app.celery beat --loglevel=info &
        BEAT_PID=$!
        echo $BEAT_PID > celery_beat.pid
        echo -e "${GREEN}✅ Celery beat started (PID: $BEAT_PID)${NC}"
    fi
}

# Start all services
echo "Starting backend server..."
start_backend

echo "Starting frontend development server..."
start_frontend

echo "Starting Celery worker and beat..."
start_celery

# Wait a moment for services to start
sleep 3

# Check if services are running
echo -e "\n${BLUE}Checking service status...${NC}"

if port_in_use 5000; then
    echo -e "${GREEN}✅ Backend API: http://localhost:5000${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
fi

if port_in_use 8080; then
    echo -e "${GREEN}✅ Frontend: http://localhost:8080${NC}"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
fi

if command_exists redis-server && port_in_use 6379; then
    echo -e "${GREEN}✅ Redis: localhost:6379${NC}"
fi

# Display useful information
echo -e "\n${BLUE}🎉 Vehicle Parking App V2 is running!${NC}"
echo "======================================"
echo -e "${GREEN}Frontend (Vue.js):${NC} http://localhost:8080"
echo -e "${GREEN}Backend API (Flask):${NC} http://localhost:5000"
if command_exists redis-server; then
    echo -e "${GREEN}Redis Cache:${NC} localhost:6379"
fi
echo ""
echo -e "${BLUE}Demo Credentials:${NC}"
echo "Admin: admin / admin123"
echo "User: john_doe / password123"
echo ""
echo -e "${YELLOW}To stop all services, run:${NC} ./stop.sh"
echo -e "${YELLOW}To view logs, check the terminal output or log files${NC}"
echo ""
echo -e "${BLUE}Happy parking! 🚗${NC}"

# Keep script running and wait for Ctrl+C
echo -e "\n${YELLOW}Press Ctrl+C to stop all services...${NC}"
trap 'echo -e "\n${BLUE}Stopping services...${NC}"; ./stop.sh; exit' INT
wait
