# 🔧 Installation Guide - Tourist Management System

## ⚠️ Fix "ModuleNotFoundError" Issue

If you see this error:
```
ModuleNotFoundError: No module named 'flask_sqlalchemy'
```

Follow these steps:

## 📝 Solution - Choose ONE method:

### Method 1: Automatic Setup (Recommended for Windows)
1. **Double-click** `setup.bat`
2. Wait for installation to complete
3. **Double-click** `run.bat` to start the application

### Method 2: Manual Installation
Open **PowerShell** or **Command Prompt** in the project folder and run:

```bash
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.1 SQLAlchemy==2.0.23
```

Then start the application:
```bash
python app.py
```

### Method 3: Using requirements.txt
```bash
pip install -r requirements.txt
```

Then:
```bash
python app.py
```

## ✅ Verify Installation

After installation, you should see:
```
Admin user created: admin@tourist.com / admin123
Database initialized with sample data!
 * Running on http://0.0.0.0:5000
```

## 🌐 Access the Application

Open your browser and go to:
- **Main Site**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

## 🔐 Login Credentials

**Admin Account:**
- Email: `admin@tourist.com`
- Password: `admin123`

**User Account:**
- Create new account via registration page

## 🐛 Still Having Issues?

### Issue: "pip is not recognized"
**Solution:** Install Python from python.org and make sure to check "Add Python to PATH" during installation.

### Issue: "Permission denied"
**Solution:** Run PowerShell/CMD as Administrator

### Issue: Python version error
**Solution:** This project requires Python 3.8 or higher. Check version:
```bash
python --version
```

### Issue: Port 5000 already in use
**Solution:** Edit `app.py`, change the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to different port
```

## 📚 Next Steps

After successful installation:
1. Create a user account
2. Browse destinations
3. Book a tour package
4. Test the payment flow
5. Login as admin to manage the system

## 💡 Tips

- Keep the terminal/command prompt window open while using the application
- Press `Ctrl+C` in the terminal to stop the server
- The database file `tourist_management.db` will be created automatically
- To reset everything, delete `tourist_management.db` and restart

## 📞 Need More Help?

Check the main README.md for:
- Complete feature list
- Database schema
- Customization guide
- Troubleshooting tips

---

**Happy Coding! 🚀**
