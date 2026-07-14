@echo off
echo ========================================
echo EMERGENCY FIX - Version Compatibility
echo ========================================
echo.
echo This will uninstall incompatible versions and install the correct ones.
echo.
pause

echo.
echo Step 1: Uninstalling current packages...
pip uninstall -y Flask Flask-SQLAlchemy Werkzeug SQLAlchemy

echo.
echo Step 2: Installing compatible versions...
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 SQLAlchemy==2.0.20

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo You can now run: python app.py
echo.
pause
