@echo off
REM Start Frontend Server Script (Windows)

echo ======================================
echo AI Supply Chain Optimizer - Frontend
echo ======================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Check for .env.local file
if not exist ".env.local" (
    echo Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo NODE_ENV=development >> .env.local
)

echo Starting Next.js frontend on http://localhost:3000
echo.
echo Make sure the backend is running on port 8000!
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause
