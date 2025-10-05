#!/bin/bash
#
# EPICcrypto Quick Preview Launch Script
# For Unix/Linux/macOS systems
#
# This script automatically:
# - Checks if Python is installed
# - Checks if dependencies are installed
# - Installs missing dependencies
# - Starts the development server
# - Opens the application in your default browser
#

set -e

echo "=================================================="
echo "🚀 EPICcrypto Quick Preview Launcher"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.11 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Check if virtual environment exists
echo "🔍 Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment exists${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies (this may take a minute)...${NC}"
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
    # Still check if all requirements are met
    echo "   Verifying all packages..."
    pip install -q -r requirements.txt
fi
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "${YELLOW}📝 Creating .env file from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created${NC}"
    else
        echo -e "${YELLOW}⚠️  No .env file found (optional)${NC}"
    fi
    echo ""
fi

# Get the port (default to 5000) and find an available one
PREFERRED_PORT=${PORT:-5000}
echo "🔍 Checking port availability..."
AVAILABLE_PORT=$(python3 find_port.py $PREFERRED_PORT 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Could not find an available port${NC}"
    echo "$AVAILABLE_PORT"
    exit 1
fi

if [ "$AVAILABLE_PORT" != "$PREFERRED_PORT" ]; then
    echo -e "${YELLOW}⚠️  Port $PREFERRED_PORT is already in use${NC}"
    echo -e "${GREEN}✅ Using alternative port: $AVAILABLE_PORT${NC}"
else
    echo -e "${GREEN}✅ Port $AVAILABLE_PORT is available${NC}"
fi
echo ""

PORT=$AVAILABLE_PORT

echo "=================================================="
echo "🎉 Starting EPICcrypto..."
echo "=================================================="
echo ""
echo "🌐 The application will open automatically in your browser"
echo "📍 URL: http://localhost:$PORT"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Wait a moment before opening browser
sleep 2

# Open browser in background based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:$PORT" &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:$PORT" &
    elif command -v gnome-open &> /dev/null; then
        gnome-open "http://localhost:$PORT" &
    fi
fi

# Start the Flask application
python3 app.py
