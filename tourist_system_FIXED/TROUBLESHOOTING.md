# 🛠️ Troubleshooting Guide

## Common Installation Errors & Solutions

### Error 1: ModuleNotFoundError: No module named 'flask_sqlalchemy'

**Cause:** Flask-SQLAlchemy is not installed

**Solution:**
```bash
pip install Flask-SQLAlchemy
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Error 2: ModuleNotFoundError: No module named 'flask'

**Solution:**
```bash
pip install Flask
```

### Error 3: "pip is not recognized as an internal or external command"

**Cause:** Python is not added to PATH or pip is not installed

**Solution:**
1. Reinstall Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Verify: `python --version` and `pip --version`

### Error 4: Permission denied

**Solution for Windows:**
- Run PowerShell or CMD as Administrator
- Right-click → "Run as administrator"

**Solution for Mac/Linux:**
```bash
sudo pip install -r requirements.txt
```

### Error 5: Port 5000 is already in use

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solution:** Edit the last line of `app.py`:
```python
# Change from:
app.run(debug=True, host='0.0.0.0', port=5000)

# To:
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: http://localhost:5001

### Error 6: Database errors

**Solution:** Delete the database and restart:
```bash
# Delete the database file
del tourist_management.db   # Windows
rm tourist_management.db    # Mac/Linux

# Run the app again
python app.py
```

### Error 7: Template not found

**Error Message:**
```
jinja2.exceptions.TemplateNotFound: login.html
```

**Solution:** Verify file structure:
```
tourist_system/
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   └── ... (all other templates)
└── static/
    └── css/
        └── style.css
```

### Error 8: CSS not loading (page looks ugly)

**Solution:**
1. Check `static/css/style.css` exists
2. Clear browser cache (Ctrl+Shift+Delete)
3. Hard refresh (Ctrl+F5)
4. Check browser console for errors (F12)

## Step-by-Step Installation (Clean Install)

### For Windows:

1. **Install Python** (if not installed)
   - Download from https://www.python.org/downloads/
   - Check "Add Python to PATH"
   - Install

2. **Extract the project**
   - Extract ZIP to a folder (e.g., `C:\Projects\tourist_system`)

3. **Open PowerShell in the project folder**
   - Hold Shift + Right-click in folder
   - Select "Open PowerShell window here"

4. **Install dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy Werkzeug SQLAlchemy
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open browser**
   - Go to http://localhost:5000

### For Mac/Linux:

1. **Install Python** (usually pre-installed)
   ```bash
   python3 --version
   ```

2. **Extract and navigate**
   ```bash
   cd /path/to/tourist_system
   ```

3. **Create virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run application**
   ```bash
   python app.py
   ```

## Verification Checklist

After installation, verify these:

- [ ] No error messages in terminal
- [ ] You see: "Running on http://0.0.0.0:5000"
- [ ] You see: "Admin user created: admin@tourist.com / admin123"
- [ ] Browser opens to login page
- [ ] CSS is loaded (page looks beautiful)
- [ ] Can create user account
- [ ] Can login as admin

## Getting Python Right

### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

Should show: Python 3.8.x or higher

### Check if pip is installed:
```bash
pip --version
# or
pip3 --version
```

### Upgrade pip (if needed):
```bash
python -m pip install --upgrade pip
```

## Environment Variables (Advanced)

If you're using a virtual environment:

### Create virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install in virtual environment:
```bash
pip install -r requirements.txt
```

### Deactivate when done:
```bash
deactivate
```

## File Permissions Issues

### Windows:
- Run as Administrator
- Disable antivirus temporarily during installation

### Mac/Linux:
```bash
chmod +x app.py
sudo chown -R $USER:$USER tourist_system/
```

## Browser Issues

### Page not loading:
1. Clear browser cache
2. Try different browser (Chrome, Firefox, Edge)
3. Disable browser extensions
4. Check firewall settings

### CSS/Images not showing:
1. Hard refresh: Ctrl+Shift+R or Cmd+Shift+R
2. Check browser console (F12) for errors
3. Verify static folder structure

## Database Reset

If the database is corrupted:

### Windows:
```bash
del tourist_management.db
python app.py
```

### Mac/Linux:
```bash
rm tourist_management.db
python app.py
```

The app will recreate everything with fresh sample data.

## Still Not Working?

### Collect Information:
1. Python version: `python --version`
2. Pip version: `pip --version`
3. Operating System: Windows/Mac/Linux
4. Error message (full text)
5. File structure (ls or dir output)

### Quick Test:
```bash
# Test if Flask is installed
python -c "import flask; print(flask.__version__)"

# Test if SQLAlchemy is installed
python -c "import flask_sqlalchemy; print('OK')"
```

## Contact & Support

If you've tried everything:
1. Check the README.md
2. Verify requirements.txt matches installed packages
3. Try clean reinstall (delete everything, extract fresh)
4. Use virtual environment to isolate dependencies

---

**Most Common Solution:** Just run `pip install -r requirements.txt` and 90% of issues will be fixed!
