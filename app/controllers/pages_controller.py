from app.controllers import bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import logout_user, current_user, login_user, login_required
from app import db
from app.models import User,Booking
from urllib.parse import urlsplit
from datetime import datetime

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('index.html', slider_cars = True)

#car
@bp.route('/cars')
def cars():
    return render_template('cars.html', title='Cars', display_cars = True)

@bp.route('/cars/list')
def cars_list():
    return render_template('cars-list.html', title='Cars List', display_cars_list = True)


@bp.route('/car/<int:id>')
def car_single_id(id):
    return render_template('car-single.html', title='Cars Single', id = id)

# user
@bp.route('/profile')
@login_required
def profile():
    return render_template('account-profile.html', title='My Profile')

@bp.route('/orders')
@login_required
def orders():
    return render_template('account-booking.html', title='My Orders')

@bp.route('/favorite')
@login_required
def favorite():
    return render_template('account-favorite.html', title='My Favorite Cars', favorite_cars = True)

#auth
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('controller.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember_me')

        user = db.session.scalar(db.select(User).from_statement(db.text(f"SELECT * FROM users WHERE username='{username}'")))
        if user is None or not user.check_password(password):
            flash('Invalid username or password.')
        else:
            login_user(user, remember = remember)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                # 檢查角色
                if user.role == 'basic':
                    next_page = url_for('controller.home')
                else:
                    next_page = url_for('controller.admin_index')

            return redirect(next_page)
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', slider_cars = True)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('controller.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        if not all([username, email, password,  re_password]):
            flash('Please fill in all required information.')
        elif User.query.filter_by(username=username).first():
            flash('This name is already in use.')
        elif User.query.filter_by(email=email).first():
            flash('This email is already in use.')
        elif password != re_password:
            flash('Passwords do not match.')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('controller.login'))

    return render_template('register.html')


@bp.route('/error')
def error():
    return render_template('errors/404.html')



#payment
@bp.route('/payment/<int:booking_id>')
def payment_page(booking_id):
    booking = db.session.query(Booking).filter_by(id=booking_id).first_or_404()
    # 檢查是否已付款，若已付款則重導向至訂單頁面
    if booking.status == 'scheduled':
        return redirect('/orders') 
    # 計算取車和還車的完整時間
    pickup_datetime = datetime.combine(booking.pickup_date, booking.pickup_time)
    return_datetime = datetime.combine(booking.return_date, booking.return_time)
    # 計算租用時數
    rental_duration = (return_datetime - pickup_datetime).total_seconds() / 3600
    return render_template('payment.html', booking=booking, rental_duration=rental_duration)
