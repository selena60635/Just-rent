import re
from app import db
from app.controllers import bp
from app.models import User
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user
from sqlalchemy import text
from functools import wraps




def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('controller.login'))
        if current_user.role != 'super_admin' and current_user.role != 'admin':
            print(current_user.role)
            return redirect(url_for('controller.home'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        if current_user.role != 'super_admin':
            flash('權限不足')
            return redirect(url_for('controller.admin_users'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/admin')
@admin_required
def admin_index():
    return render_template('admin/index.html')

@bp.route('/admin/cars')
@admin_required
def admin_cars():
    sql = text('SELECT * FROM cars')
    result = db.session.execute(sql)
    cars = []
    for row in result:
        cars.append(row)
    return render_template('admin/cars.html', cars=cars)

@bp.route('/admin/car/<int:id>')
@admin_required
def admin_get_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    return render_template('admin/car.html', car=car)

@bp.route('/admin/edit_car/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    if request.method == 'POST':
        name = request.form.get('name')
        seat = request.form.get('seat')
        door = request.form.get('door')
        body = request.form.get('body')
        powerType = request.form.get('power-type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        year = request.form.get('year')
        price = request.form.get('price')
        # 處理int部分
        displacement_raw = re.search(r'\d+', request.form.get('displacement'))
        displacement = int(displacement_raw.group()) if displacement_raw else None
        carLength_raw = re.search(r'\d+', request.form.get('car-length'))
        carLength = int(carLength_raw.group()) if carLength_raw else None
        wheelbase_raw =  re.search(r'\d+', request.form.get('wheelbase'))
        wheelbase = int(wheelbase_raw.group()) if wheelbase_raw else None

        update_query = text("UPDATE cars SET name = :name, seat = :seat, door = :door, body = :body, "
                            "displacement = :displacement, car_length = :carLength, wheelbase = :wheelbase, "
                            "power_type = :powerType, brand = :brand, model = :model, year = :year, price = :price WHERE id = :car_id")

        db.session.execute(update_query, {'name': name, 'seat': seat, 'door': door, 'body': body,
                                           'displacement': displacement, 'carLength': carLength,
                                           'wheelbase': wheelbase, 'powerType': powerType, 'brand': brand, 'model': model, 'year': year, 'price': price,
                                           'car_id': id})
        db.session.commit()
        updated_result = db.session.execute(sql, {'car_id': id})
        updated_car = updated_result.fetchone()

        return render_template('admin/edit_car.html', car=updated_car)
    return render_template('admin/edit_car.html', car=car)

@bp.route('/admin/logout')
@admin_required
def admin_logout():
    logout_user()
    return redirect(url_for('controller.admin_index'))


@bp.route('/admin/users')
@admin_required
def admin_users():
    sql = text('SELECT * FROM users')
    result = db.session.execute(sql)
    users = []
    for row in result:
        users.append(row)
    return render_template('admin/users.html', users=users)

@bp.route('/admin/user/<int:id>')
@admin_required
def admin_get_user(id):
    sql = text('SELECT * FROM users WHERE id = :user_id')
    result = db.session.execute(sql, {'user_id': id})
    user = result.fetchone()
    return render_template('admin/user.html', user=user)

@bp.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
@super_admin_required
def admin_edit_user(id):
    sql = text('SELECT * FROM users WHERE id = :user_id')
    result = db.session.execute(sql, {'user_id': id})
    user = result.fetchone()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone') 
        language = request.form.get('language')
        hour_format = request.form.get('hour_format')
        role = request.form.get('role')

        update_query = text("UPDATE users SET username = :username, email = :email, phone = :phone, language = :language, "
                            "hour_format = :hour_format, role = :role WHERE id = :user_id")

        db.session.execute(update_query, {'username': username, 'email': email, 'phone': phone, 'language': language,
                                           'hour_format': hour_format, 'role': role, 'user_id': id})
        db.session.commit()
        updated_result = db.session.execute(sql, {'user_id': id})
        updated_user = updated_result.fetchone()

        return render_template('admin/edit_user.html', user=updated_user)
    return render_template('admin/edit_user.html', user=user)

