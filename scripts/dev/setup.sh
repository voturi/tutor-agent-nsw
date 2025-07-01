#!/bin/bash

# TutorAgent MVP Development Setup Script
echo "🔧 Setting up TutorAgent development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python 3.11+ is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $python_version found"
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check if Docker is installed
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    print_status "Docker found"
else
    print_warning "Docker not found. You can still run locally without Docker."
fi

# Create Python virtual environment
echo "Setting up Python virtual environment..."
cd "$(dirname "$0")/../.." # Go to project root

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install backend dependencies
pip install -r backend/requirements.txt
print_status "Backend dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env file from example. Please update with your actual values."
else
    print_status ".env file already exists"
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p data/{uploads,processed}
print_status "Directories created"

# Check if Node.js is installed for frontend (future)
echo "Checking Node.js for frontend development..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    print_status "Node.js $node_version found"
else
    print_warning "Node.js not found. Install Node.js 18+ for frontend development."
fi

# Download spaCy model
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm
print_status "spaCy model downloaded"

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys and configuration"
echo "2. Start the services:"
echo "   • For local development: ./scripts/dev/start-local.sh"
echo "   • For Docker development: docker-compose up"
echo ""
echo "3. Visit http://localhost:8000/docs to see the API documentation"
echo ""
print_warning "Remember to activate the virtual environment: source venv/bin/activate"
