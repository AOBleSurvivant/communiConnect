@echo off
title CommuniConnect - Start

echo.
echo ========================================
echo    COMMUNICONNECT - START SERVER
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Vérifier Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js
    pause
    exit /b 1
)

echo [OK] Python and Node.js detected
echo.

REM Backend setup
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment if not exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo [INFO] Running database migrations...
python manage.py makemigrations
python manage.py migrate

cd ..

REM Frontend setup
echo [INFO] Setting up frontend...
cd frontend

REM Install dependencies if not exists
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    npm install
)

cd ..

echo.
echo [INFO] Starting servers...
echo.

REM Start backend
echo [INFO] Starting Django backend...
start "Django Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python manage.py runserver 8000"

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Start frontend
echo [INFO] Starting React frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo    SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/api/schema/
echo.
echo Press any key to close this window...
pause >nul 