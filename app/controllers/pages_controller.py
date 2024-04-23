from app.controllers import bp
from flask import render_template

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('index.html', title='Home')

@bp.route('/cars')
def cars():
    return render_template('cars.html', title='Cars')

@bp.route('/cars/list')
def cars_list():
    return render_template('cars-list.html', title='Cars List')

# @bp.route('/cars/<int:id>')
@bp.route('/cars/single')
def cars_single():
    return render_template('car-single.html', title='Cars Single',  car_id = 'car_id')

@bp.route('/booking')
def booking():
    return render_template('booking.html', title='Booking')

# user
@bp.route('/profile')
def profile():
    return render_template('account-profile.html', title='My Profile')

@bp.route('/orders')
def orders():
    return render_template('account-booking.html', title='My Orders')

@bp.route('/favorite')
def favorite():
    return render_template('account-favorite.html', title='My Favorite Cars')


@bp.route('/login')
def login():
    return render_template('login.html', title='Login')

@bp.route('/register')
def register():
    return render_template('register.html', title='Register')


@bp.route('/error')
def error():
    return render_template('errors/404.html')

