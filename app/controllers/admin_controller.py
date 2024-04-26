import re
from app import db
from app.controllers import bp
from flask import render_template, request
from sqlalchemy import text

@bp.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@bp.route('/admin/cars')
def admin_cars():
    sql = text('SELECT * FROM cars')
    result = db.session.execute(sql)
    cars = []
    for row in result:
        cars.append(row)
    return render_template('admin/cars.html', cars=cars)

@bp.route('/admin/car/<int:id>')
def admin_get_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    return render_template('admin/car.html', car=car)

@bp.route('/admin/edit_car/<int:id>', methods=['GET', 'POST'])
def admin_edit_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    if request.method == 'POST':
        carName = request.form.get('car-name')
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

        update_query = text("UPDATE cars SET car_name = :carName, seat = :seat, door = :door, body = :body, "
                            "displacement = :displacement, car_length = :carLength, wheelbase = :wheelbase, "
                            "power_type = :powerType, brand = :brand, model = :model, year = :year, price = :price WHERE id = :car_id")

        db.session.execute(update_query, {'carName': carName, 'seat': seat, 'door': door, 'body': body,
                                           'displacement': displacement, 'carLength': carLength,
                                           'wheelbase': wheelbase, 'powerType': powerType, 'brand': brand, 'model': model, 'year': year, 'price': price,
                                           'car_id': id})
        db.session.commit()
        updated_result = db.session.execute(sql, {'car_id': id})
        updated_car = updated_result.fetchone()

        return render_template('admin/edit_car.html', car=updated_car)
    return render_template('admin/edit_car.html', car=car)

