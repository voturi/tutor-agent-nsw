#!/bin/bash

# TutorAgent MVP Local Development Startup Script
echo "🚀 Starting TutorAgent MVP locally..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Go to project root
cd "$(dirname "$0")/../.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup first:"
    echo "./scripts/dev/setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating from example..."
    cp .env.example .env
    echo "Please update .env with your actual values before continuing."
    exit 1
fi

# Export environment variables
export $(cat .env | grep -v ^# | xargs)
print_status "Environment variables loaded"

# Start PostgreSQL and Redis using Docker (if Docker is available)
if command -v docker &> /dev/null; then
    echo "Starting PostgreSQL and Redis with Docker..."
    docker-compose up -d postgres redis
    print_status "Database services started"
    
    # Wait for services to be ready
    echo "Waiting for services to be ready..."
    sleep 5
else
    print_warning "Docker not found. Make sure PostgreSQL and Redis are running locally."
fi

# Start the FastAPI application
echo "Starting TutorAgent backend..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info

print_status "TutorAgent MVP is running!"
echo "🌐 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "🔧 ReDoc: http://localhost:8000/redoc"
