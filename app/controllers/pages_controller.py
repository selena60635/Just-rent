from app.controllers import bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import logout_user, current_user, login_user, login_required
from app import db
from app.models import User
from urllib.parse import urlsplit

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('index.html', slider_cars = True)

@bp.route('/cars')
def cars():
    return render_template('cars.html', title='Cars', display_cars = True)

@bp.route('/cars/list')
def cars_list():
    return render_template('cars-list.html', title='Cars List', display_cars_list = True)

@bp.route('/car/single')
def car_single():
    return render_template('car-single.html', title='Cars Single')

@bp.route('/car/<int:id>')
def car_single_id(id):
    return render_template('car-single.html', title='Cars Single', id = id)

@bp.route('/booking')
@login_required
def booking():
    return render_template('booking.html', title='Booking')

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
    return render_template('account-favorite.html', title='My Favorite Cars')


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
            flash('無效的使用者名稱或密碼')
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
    return render_template('index.html')

@bp.route('/register')
def register():
    return render_template('register.html', title='Register')


@bp.route('/error')
def error():
    return render_template('errors/404.html')

