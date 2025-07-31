#!/bin/bash

# Vehicle Parking App V2 - Stop Script
# This script stops all running services

echo "🛑 Stopping Vehicle Parking App V2..."
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to stop process by PID file
stop_process() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $service_name (PID: $pid)...${NC}"
            kill $pid
            
            # Wait for process to stop
            local count=0
            while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                count=$((count + 1))
            done
            
            if ps -p $pid > /dev/null 2>&1; then
                echo -e "${RED}Force stopping $service_name...${NC}"
                kill -9 $pid
            else
                echo -e "${GREEN}✅ $service_name stopped${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  $service_name was not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}⚠️  No PID file found for $service_name${NC}"
    fi
}

# Stop backend
if [ -f "backend/backend.pid" ]; then
    stop_process "Backend" "backend/backend.pid"
else
    # Try to find and stop Flask process
    FLASK_PID=$(pgrep -f "python.*run.py")
    if [ ! -z "$FLASK_PID" ]; then
        echo -e "${YELLOW}Stopping Flask backend (PID: $FLASK_PID)...${NC}"
        kill $FLASK_PID
        echo -e "${GREEN}✅ Backend stopped${NC}"
    fi
fi

# Stop frontend
if [ -f "frontend/frontend.pid" ]; then
    stop_process "Frontend" "frontend/frontend.pid"
else
    # Try to find and stop Vue.js dev server
    VUE_PID=$(pgrep -f "vue-cli-service serve")
    if [ ! -z "$VUE_PID" ]; then
        echo -e "${YELLOW}Stopping Vue.js frontend (PID: $VUE_PID)...${NC}"
        kill $VUE_PID
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
fi

# Stop Celery worker
if [ -f "backend/celery.pid" ]; then
    stop_process "Celery Worker" "backend/celery.pid"
else
    # Try to find and stop Celery worker
    CELERY_PID=$(pgrep -f "celery.*worker")
    if [ ! -z "$CELERY_PID" ]; then
        echo -e "${YELLOW}Stopping Celery worker (PID: $CELERY_PID)...${NC}"
        kill $CELERY_PID
        echo -e "${GREEN}✅ Celery worker stopped${NC}"
    fi
fi

# Stop Celery beat
if [ -f "backend/celery_beat.pid" ]; then
    stop_process "Celery Beat" "backend/celery_beat.pid"
else
    # Try to find and stop Celery beat
    BEAT_PID=$(pgrep -f "celery.*beat")
    if [ ! -z "$BEAT_PID" ]; then
        echo -e "${YELLOW}Stopping Celery beat (PID: $BEAT_PID)...${NC}"
        kill $BEAT_PID
        echo -e "${GREEN}✅ Celery beat stopped${NC}"
    fi
fi

# Stop any remaining processes on the ports
echo -e "\n${BLUE}Checking for processes on app ports...${NC}"

# Check port 5000 (Backend)
BACKEND_PORT_PID=$(lsof -ti:5000)
if [ ! -z "$BACKEND_PORT_PID" ]; then
    echo -e "${YELLOW}Stopping process on port 5000 (PID: $BACKEND_PORT_PID)...${NC}"
    kill $BACKEND_PORT_PID
fi

# Check port 8080 (Frontend)
FRONTEND_PORT_PID=$(lsof -ti:8080)
if [ ! -z "$FRONTEND_PORT_PID" ]; then
    echo -e "${YELLOW}Stopping process on port 8080 (PID: $FRONTEND_PORT_PID)...${NC}"
    kill $FRONTEND_PORT_PID
fi

# Clean up any remaining PID files
rm -f backend/backend.pid frontend/frontend.pid backend/celery.pid backend/celery_beat.pid

# Note about Redis
echo -e "\n${BLUE}Note:${NC} Redis server is left running as it may be used by other applications."
echo -e "To stop Redis manually: ${YELLOW}redis-cli shutdown${NC}"

echo -e "\n${GREEN}✅ All Vehicle Parking App services stopped!${NC}"
echo "============================================"
