#!/bin/bash

# Start Backend Server Script

echo "======================================"
echo "AI Supply Chain Optimizer - Backend"
echo "======================================"
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo ""
    echo "OPENAI_API_KEY=your_key_here"
    echo "GOOGLE_MAPS_API_KEY=your_key_here"
    echo "WEATHER_API_KEY=your_key_here"
    echo ""
    echo "Continuing without API keys (limited functionality)..."
    echo ""
fi

echo "Starting FastAPI backend on http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
