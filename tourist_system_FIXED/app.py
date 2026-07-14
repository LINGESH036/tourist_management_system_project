from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tourist_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# Database Models
# ─────────────────────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    transports = db.relationship('Transport', backref='user', lazy=True)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    package_type = db.Column(db.String(50), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'))
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    destination = db.relationship('Destination', backref='packages')
    bookings = db.relationship('Booking', backref='package', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    num_people = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment = db.relationship('Payment', backref='booking', uselist=False, lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    card_holder_name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='completed')
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transport_type = db.Column(db.String(50), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    drop_location = db.Column(db.String(200), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper
def admin_required():
    return 'user_id' in session and session.get('is_admin')

# ─────────────────────────────────────────────
# Public / User Routes
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard') if user.is_admin else url_for('destinations'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        new_user = User(full_name=full_name, email=email,
                        password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/destinations')
def destinations():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_destinations = Destination.query.all()
    categories = db.session.query(Destination.category).distinct().all()
    return render_template('destinations.html', destinations=all_destinations, categories=categories)

@app.route('/packages')
def packages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_packages = Package.query.all()
    package_types = db.session.query(Package.package_type).distinct().all()
    return render_template('packages.html', packages=all_packages, package_types=package_types)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        package_id = request.form.get('package_id')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        num_people = int(request.form.get('num_people', 1))
        package = Package.query.get(package_id)
        total_amount = package.price * num_people
        new_booking = Booking(user_id=session['user_id'], package_id=package_id,
                              full_name=full_name, email=email,
                              travel_date=travel_date, num_people=num_people,
                              total_amount=total_amount)
        db.session.add(new_booking)
        db.session.commit()
        session['booking_id'] = new_booking.id
        flash('Booking submitted successfully!', 'success')
        return redirect(url_for('payment'))
    all_packages = Package.query.all()
    return render_template('booking.html', packages=all_packages)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        booking_id = session.get('booking_id')
        if not booking_id:
            flash('No booking found!', 'error')
            return redirect(url_for('booking'))
        bk = Booking.query.get(booking_id)
        card_holder_name = request.form.get('card_holder_name')
        card_number = request.form.get('card_number')
        new_payment = Payment(booking_id=booking_id,
                              card_holder_name=card_holder_name,
                              card_number=card_number[-4:].rjust(len(card_number), '*'),
                              amount=bk.total_amount)
        bk.status = 'confirmed'
        db.session.add(new_payment)
        db.session.commit()
        session.pop('booking_id', None)
        flash('Payment successful! Your booking is confirmed.', 'success')
        return redirect(url_for('my_bookings'))
    booking_id = session.get('booking_id')
    bk = Booking.query.get(booking_id) if booking_id else None
    return render_template('payment.html', booking=bk)

@app.route('/transport', methods=['GET', 'POST'])
def transport():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_t = Transport(
            user_id=session['user_id'],
            transport_type=request.form.get('transport_type'),
            pickup_location=request.form.get('pickup_location'),
            drop_location=request.form.get('drop_location'),
            travel_date=datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        )
        db.session.add(new_t)
        db.session.commit()
        flash('Transportation booked successfully!', 'success')
        return redirect(url_for('transport'))
    return render_template('transport.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_review = Review(user_id=session['user_id'],
                            name=request.form.get('name'),
                            review_text=request.form.get('review_text'),
                            rating=int(request.form.get('rating', 5)))
        db.session.add(new_review)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('review'))
    reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    return render_template('review.html', reviews=reviews)

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    bkgs = Booking.query.filter_by(user_id=session['user_id'])\
                        .order_by(Booking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bkgs)

# ─────────────────────────────────────────────
# Admin Login
# ─────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials', 'error')
    return render_template('admin_login.html')

# ─────────────────────────────────────────────
# Admin Dashboard
# ─────────────────────────────────────────────
@app.route('/admin/dashboard')
def admin_dashboard():
    if not admin_required():
        return redirect(url_for('admin_login'))
    total_users = User.query.filter_by(is_admin=False).count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    pending_bookings = Booking.query.filter_by(status='pending').count()
    total_destinations = Destination.query.count()
    total_packages = Package.query.count()
    total_reviews = Review.query.count()
    total_transports = Transport.query.count()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html',
                           total_users=total_users, total_bookings=total_bookings,
                           total_revenue=total_revenue, pending_bookings=pending_bookings,
                           total_destinations=total_destinations, total_packages=total_packages,
                           total_reviews=total_reviews, total_transports=total_transports,
                           recent_bookings=recent_bookings)

# ─────────────────────────────────────────────
# Admin Destinations  CRUD
# ─────────────────────────────────────────────
@app.route('/admin/destinations', methods=['GET', 'POST'])
def admin_destinations():
    if not admin_required():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        db.session.add(Destination(
            name=request.form.get('name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url')
        ))
        db.session.commit()
        flash('Destination added successfully!', 'success')
        return redirect(url_for('admin_destinations'))
    all_dest = Destination.query.order_by(Destination.created_at.desc()).all()
    return render_template('admin_destinations.html', destinations=all_dest)

@app.route('/admin/destinations/edit/<int:id>', methods=['GET', 'POST'])
def admin_destinations_edit(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    dest = Destination.query.get_or_404(id)
    if request.method == 'POST':
        dest.name = request.form.get('name')
        dest.category = request.form.get('category')
        dest.description = request.form.get('description')
        dest.image_url = request.form.get('image_url')
        db.session.commit()
        flash('Destination updated successfully!', 'success')
        return redirect(url_for('admin_destinations'))
    return render_template('admin_destinations_edit.html', destination=dest)

@app.route('/admin/destinations/delete/<int:id>', methods=['POST'])
def admin_destinations_delete(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    dest = Destination.query.get_or_404(id)
    Package.query.filter_by(destination_id=id).update({'destination_id': None})
    db.session.delete(dest)
    db.session.commit()
    flash('Destination deleted successfully!', 'success')
    return redirect(url_for('admin_destinations'))

# ─────────────────────────────────────────────
# Admin Packages  CRUD
# ─────────────────────────────────────────────
@app.route('/admin/packages', methods=['GET', 'POST'])
def admin_packages():
    if not admin_required():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        db.session.add(Package(
            name=request.form.get('name'),
            package_type=request.form.get('package_type'),
            destination_id=request.form.get('destination_id') or None,
            price=float(request.form.get('price', 0)),
            duration=request.form.get('duration'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url')
        ))
        db.session.commit()
        flash('Package added successfully!', 'success')
        return redirect(url_for('admin_packages'))
    all_pkg = Package.query.order_by(Package.created_at.desc()).all()
    all_dest = Destination.query.all()
    return render_template('admin_packages.html', packages=all_pkg, destinations=all_dest)

@app.route('/admin/packages/edit/<int:id>', methods=['GET', 'POST'])
def admin_packages_edit(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    pkg = Package.query.get_or_404(id)
    if request.method == 'POST':
        pkg.name = request.form.get('name')
        pkg.package_type = request.form.get('package_type')
        pkg.destination_id = request.form.get('destination_id') or None
        pkg.price = float(request.form.get('price', 0))
        pkg.duration = request.form.get('duration')
        pkg.description = request.form.get('description')
        pkg.image_url = request.form.get('image_url')
        db.session.commit()
        flash('Package updated successfully!', 'success')
        return redirect(url_for('admin_packages'))
    all_dest = Destination.query.all()
    return render_template('admin_packages_edit.html', package=pkg, destinations=all_dest)

@app.route('/admin/packages/delete/<int:id>', methods=['POST'])
def admin_packages_delete(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    pkg = Package.query.get_or_404(id)
    db.session.delete(pkg)
    db.session.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('admin_packages'))

# ─────────────────────────────────────────────
# Admin Bookings  CRUD
# ─────────────────────────────────────────────
@app.route('/admin/bookings')
def admin_bookings():
    if not admin_required():
        return redirect(url_for('admin_login'))
    all_bk = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin_bookings.html', bookings=all_bk)

@app.route('/admin/bookings/edit/<int:id>', methods=['GET', 'POST'])
def admin_bookings_edit(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    bk = Booking.query.get_or_404(id)
    if request.method == 'POST':
        bk.full_name = request.form.get('full_name')
        bk.email = request.form.get('email')
        bk.travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        bk.num_people = int(request.form.get('num_people', 1))
        bk.status = request.form.get('status')
        pkg = Package.query.get(bk.package_id)
        if pkg:
            bk.total_amount = pkg.price * bk.num_people
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('admin_bookings'))
    return render_template('admin_bookings_edit.html', booking=bk)

@app.route('/admin/bookings/update-status/<int:id>', methods=['POST'])
def admin_booking_update_status(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    bk = Booking.query.get_or_404(id)
    bk.status = request.form.get('status')
    db.session.commit()
    flash('Booking status updated!', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/bookings/delete/<int:id>', methods=['POST'])
def admin_bookings_delete(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    bk = Booking.query.get_or_404(id)
    if bk.payment:
        db.session.delete(bk.payment)
    db.session.delete(bk)
    db.session.commit()
    flash('Booking deleted successfully!', 'success')
    return redirect(url_for('admin_bookings'))

# ─────────────────────────────────────────────
# Admin Reviews  CRUD
# ─────────────────────────────────────────────
@app.route('/admin/reviews')
def admin_reviews():
    if not admin_required():
        return redirect(url_for('admin_login'))
    all_rev = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin_reviews.html', reviews=all_rev)

@app.route('/admin/reviews/edit/<int:id>', methods=['GET', 'POST'])
def admin_reviews_edit(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    rev = Review.query.get_or_404(id)
    if request.method == 'POST':
        rev.name = request.form.get('name')
        rev.review_text = request.form.get('review_text')
        rev.rating = int(request.form.get('rating', 5))
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('admin_reviews'))
    return render_template('admin_reviews_edit.html', review=rev)

@app.route('/admin/reviews/delete/<int:id>', methods=['POST'])
def admin_reviews_delete(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    rev = Review.query.get_or_404(id)
    db.session.delete(rev)
    db.session.commit()
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('admin_reviews'))

# ─────────────────────────────────────────────
# Admin Transport  CRUD
# ─────────────────────────────────────────────
@app.route('/admin/transport')
def admin_transport():
    if not admin_required():
        return redirect(url_for('admin_login'))
    all_t = Transport.query.order_by(Transport.created_at.desc()).all()
    return render_template('admin_transport.html', transports=all_t)

@app.route('/admin/transport/add', methods=['GET', 'POST'])
def admin_transport_add():
    if not admin_required():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_t = Transport(
            user_id=user_id,
            transport_type=request.form.get('transport_type'),
            pickup_location=request.form.get('pickup_location'),
            drop_location=request.form.get('drop_location'),
            travel_date=datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date(),
            status=request.form.get('status', 'pending')
        )
        db.session.add(new_t)
        db.session.commit()
        flash('Transport booking added successfully!', 'success')
        return redirect(url_for('admin_transport'))
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin_transport_add.html', users=users)

@app.route('/admin/transport/edit/<int:id>', methods=['GET', 'POST'])
def admin_transport_edit(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    t = Transport.query.get_or_404(id)
    if request.method == 'POST':
        t.transport_type = request.form.get('transport_type')
        t.pickup_location = request.form.get('pickup_location')
        t.drop_location = request.form.get('drop_location')
        t.travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        t.status = request.form.get('status')
        db.session.commit()
        flash('Transport updated successfully!', 'success')
        return redirect(url_for('admin_transport'))
    return render_template('admin_transport_edit.html', transport=t)

@app.route('/admin/transport/delete/<int:id>', methods=['POST'])
def admin_transport_delete(id):
    if not admin_required():
        return redirect(url_for('admin_login'))
    t = Transport.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('Transport deleted successfully!', 'success')
    return redirect(url_for('admin_transport'))

# ─────────────────────────────────────────────
# Database Initialisation
# ─────────────────────────────────────────────
def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@tourist.com').first():
            db.session.add(User(full_name='Admin User', email='admin@tourist.com',
                                password=generate_password_hash('admin123'), is_admin=True))
            db.session.commit()
            print("Admin user created: admin@tourist.com / admin123")
        if Destination.query.count() == 0:
            db.session.add_all([
                Destination(name='Goa', category='Beach Destinations',
                            description='Beautiful beaches and vibrant nightlife',
                            image_url='https://images.unsplash.com/photo-1512343879784-a960bf40e7f2'),
                Destination(name='Manali', category='Hill Stations',
                            description='Scenic mountains and adventure activities',
                            image_url='https://images.unsplash.com/photo-1626621341517-bbf3d9990a23'),
                Destination(name='Agra', category='Historical Places',
                            description='Home to the magnificent Taj Mahal',
                            image_url='https://images.unsplash.com/photo-1564507592333-c60657eea523'),
                Destination(name='Paris', category='International Destinations',
                            description='City of lights and romance',
                            image_url='https://images.unsplash.com/photo-1502602898657-3e91760cbb34'),
                Destination(name='Dubai', category='International Destinations',
                            description='Luxury shopping and modern architecture',
                            image_url='https://images.unsplash.com/photo-1512453979798-5ea266f8880c'),
            ])
            db.session.commit()
        if Package.query.count() == 0:
            db.session.add_all([
                Package(name='Goa Beach Paradise', package_type='Family Package',
                        destination_id=1, price=25000, duration='5 Days / 4 Nights',
                        description='Enjoy the sun, sand and sea with your family',
                        image_url='https://images.unsplash.com/photo-1559827260-dc66d52bef19'),
                Package(name='Manali Adventure Special', package_type='Adventure Package',
                        destination_id=2, price=35000, duration='6 Days / 5 Nights',
                        description='Trekking, paragliding and mountain adventures',
                        image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4'),
                Package(name='Paris Honeymoon', package_type='Honeymoon Package',
                        destination_id=4, price=150000, duration='7 Days / 6 Nights',
                        description='Romantic getaway in the city of love',
                        image_url='https://images.unsplash.com/photo-1511739001486-6bfe10ce785f'),
                Package(name='Dubai Luxury Experience', package_type='Luxury Package',
                        destination_id=5, price=120000, duration='5 Days / 4 Nights',
                        description='Experience luxury and modern marvels',
                        image_url='https://images.unsplash.com/photo-1518684079-3c830dcef090'),
            ])
            db.session.commit()
        print("Database initialised!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
