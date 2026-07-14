@echo off
echo ========================================
echo  Tourist Management System - Setup
echo ========================================
echo.

REM Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing dependencies...
python -m pip install "Flask>=3.0.0" "Flask-SQLAlchemy>=3.1.0" "Werkzeug>=3.0.0" "SQLAlchemy>=2.0.30"

echo.
echo [3/3] Dependencies installed successfully!
echo.
echo ========================================
echo  Run the app with:  python app.py
echo  Then open:         http://localhost:5000
echo  Admin login:       admin@tourist.com
echo  Admin password:    admin123
echo ========================================
pause
