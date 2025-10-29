#!/bin/bash

# Start Frontend Server Script

echo "======================================"
echo "AI Supply Chain Optimizer - Frontend"
echo "======================================"
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check for .env.local file
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo "NODE_ENV=development" >> .env.local
fi

echo "Starting Next.js frontend on http://localhost:3000"
echo ""
echo "Make sure the backend is running on port 8000!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
