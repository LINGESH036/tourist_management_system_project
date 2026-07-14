# 🌍 Wanderlust - Tourist Management System

A comprehensive web-based tourist management system built with Flask, SQLite, and modern web technologies. Features elegant design, complete booking workflow, and admin management capabilities.

## ✨ Features

### User Features
- 🔐 User Registration & Authentication
- 🗺️ Browse Destinations by Category
- 📦 Explore Tour Packages
- 🎫 Book Tours with Date Selection
- 💳 Secure Payment Processing
- 🚌 Transportation Booking
- ⭐ Submit Reviews & Feedback
- 📋 View Booking History

### Admin Features
- 📊 Analytics Dashboard
- ➕ Add/Manage Destinations
- 📦 Create/Manage Tour Packages
- 📖 View All Bookings
- ⭐ Monitor Customer Reviews
- 🚌 Manage Transportation Requests

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Custom CSS with Google Fonts (Cormorant Garamond, Raleway)
- **Icons**: Font Awesome 6.4.0
- **Images**: Unsplash API

## 📁 Project Structure

```
tourist_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── tourist_management.db       # SQLite database (auto-generated)
├── static/
│   └── css/
│       └── style.css          # Main stylesheet
└── templates/
    ├── base.html              # Base template with navigation
    ├── login.html             # User login page
    ├── register.html          # User registration page
    ├── destinations.html      # Browse destinations
    ├── packages.html          # Tour packages
    ├── booking.html           # Booking form
    ├── payment.html           # Payment processing
    ├── transport.html         # Transport booking
    ├── review.html            # Customer reviews
    ├── my_bookings.html       # User booking history
    ├── admin_login.html       # Admin login
    ├── admin_dashboard.html   # Admin dashboard
    ├── admin_destinations.html # Manage destinations
    ├── admin_packages.html    # Manage packages
    ├── admin_bookings.html    # View all bookings
    ├── admin_reviews.html     # View reviews
    └── admin_transport.html   # Manage transport
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Extract the Project
```bash
cd tourist_system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will:
- Initialize the SQLite database
- Create sample destinations and packages
- Create default admin user
- Start the development server on `http://localhost:5000`

### Step 5: Access the Application
Open your browser and navigate to:
- **User Interface**: http://localhost:5000
- **Admin Interface**: http://localhost:5000/admin/login

## 👤 Default Login Credentials

### Admin Login
- **Email**: admin@tourist.com
- **Password**: admin123

### Create User Account
Use the registration page to create a new user account.

## 📊 Database Schema

### Tables
1. **User** - User accounts and admin users
2. **Destination** - Tourist destinations
3. **Package** - Tour packages
4. **Booking** - Tour bookings
5. **Payment** - Payment records
6. **Transport** - Transportation bookings
7. **Review** - Customer reviews

## 🎨 Design Features

- **Modern Aesthetics**: Custom gradient backgrounds and elegant typography
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Smooth Animations**: Fade-in effects and hover transitions
- **Color Palette**: 
  - Primary: Purple gradient (#667eea to #764ba2)
  - Secondary: Ocean blue (#004E89)
  - Accent: Golden yellow (#F7B801)
  - Success: Teal green (#2A9D8F)

## 🔒 Security Features

- Password hashing using Werkzeug security
- Session-based authentication
- Protected admin routes
- SQL injection prevention via SQLAlchemy ORM
- Card number masking in payment records

## 📝 Usage Guide

### For Users

1. **Register/Login**
   - Create an account or login with existing credentials
   - Access will be granted to browse destinations and packages

2. **Browse Destinations**
   - View all available destinations with images and descriptions
   - Organized by categories (Beach, Hill Stations, Historical, etc.)

3. **Select Package**
   - Browse tour packages with pricing and duration
   - Filter by package type (Family, Honeymoon, Adventure, etc.)

4. **Make Booking**
   - Select package, travel date, and number of people
   - View total cost before proceeding
   - Complete payment securely

5. **Book Transport**
   - Select transport type
   - Enter pickup and drop locations
   - Choose travel date

6. **Submit Reviews**
   - Share your experience
   - Rate your tour (1-5 stars)

### For Administrators

1. **Login to Admin Panel**
   - Use admin credentials to access dashboard
   - View system statistics and recent bookings

2. **Manage Destinations**
   - Add new destinations with images
   - Categorize destinations
   - View all existing destinations

3. **Manage Packages**
   - Create tour packages
   - Set pricing and duration
   - Link to destinations

4. **Monitor Bookings**
   - View all customer bookings
   - Track booking status
   - Monitor revenue

5. **View Reviews**
   - Read customer feedback
   - Monitor satisfaction ratings

## 🔧 Customization

### Adding New Destinations
1. Login as admin
2. Navigate to "Destinations" in admin panel
3. Fill in destination details
4. Use Unsplash URLs for high-quality images

### Creating Packages
1. Login as admin
2. Navigate to "Packages" in admin panel
3. Select destination and package type
4. Set price and duration
5. Add package description and image

### Modifying Styles
Edit `static/css/style.css` to customize:
- Colors (CSS variables in `:root`)
- Fonts
- Layouts
- Animations

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors, delete `tourist_management.db` and restart the application. It will recreate the database with sample data.

### Port Already in Use
If port 5000 is occupied, modify the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
```

### Missing Dependencies
Ensure all packages are installed:
```bash
pip install -r requirements.txt --upgrade
```

## 📦 Sample Data

The system comes pre-loaded with:
- 5 sample destinations (Goa, Manali, Agra, Paris, Dubai)
- 4 sample packages
- 1 admin user account

## 🌟 Future Enhancements

Potential features for future development:
- Email notifications
- Payment gateway integration
- Multi-language support
- Advanced search and filters
- User profile management
- Booking cancellation
- PDF invoice generation
- Real-time chat support
- Social media integration
- Mobile application

## 📄 License

This project is created for educational purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Verify all dependencies are installed

## 🎉 Credits

- **Images**: Unsplash
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Cormorant Garamond, Raleway)
- **Framework**: Flask

---

**Built with ❤️ for travelers around the world**

🌍 Wanderlust - Explore the world with confidence!
