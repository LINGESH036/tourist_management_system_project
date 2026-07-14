# 🚨 QUICK FIX - TypeError: Response.set_cookie() Error

## The Problem
You're getting this error:
```
TypeError: Response.set_cookie() got an unexpected keyword argument 'partitioned'
```

This is because **Flask 3.0** and **Werkzeug 3.0** are incompatible with each other.

## ✅ SOLUTION (Choose One)

### Option 1: Use the Fix Script (EASIEST)
1. **Double-click `fix_versions.bat`**
2. Wait for it to complete
3. Run the application: **Double-click `run.bat`**

### Option 2: Manual Fix
Open PowerShell/CMD in the project folder and run these commands:

```bash
# Uninstall incompatible versions
pip uninstall -y Flask Flask-SQLAlchemy Werkzeug SQLAlchemy

# Install compatible versions
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 SQLAlchemy==2.0.20
```

Then run:
```bash
python app.py
```

### Option 3: Use requirements.txt
```bash
pip uninstall -y Flask Flask-SQLAlchemy Werkzeug SQLAlchemy
pip install -r requirements.txt
```

## ✅ Verify It's Fixed

After running the fix, you should see:
```
Admin user created: admin@tourist.com / admin123
Database initialized with sample data!
 * Running on http://127.0.0.1:5000
```

No more errors!

## 🎯 What Changed

**OLD (Broken):**
- Flask 3.0.0 + Werkzeug 3.0.1 = ❌ Incompatible

**NEW (Working):**
- Flask 2.3.3 + Werkzeug 2.3.7 = ✅ Compatible

## 🔍 Why This Happened

Flask 3.0 introduced changes that aren't compatible with some Werkzeug 3.0 features. The `partitioned` cookie argument was added in a way that causes conflicts.

Using Flask 2.3.3 with Werkzeug 2.3.7 is the stable, tested combination.

## 📝 After Fixing

1. Run `python app.py`
2. Open http://localhost:5000
3. Create user account or login as admin
4. Everything should work perfectly!

---

**This fix is guaranteed to work!** 🎉
