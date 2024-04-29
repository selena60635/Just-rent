from app import db
from app.api import bp
from flask import jsonify
from sqlalchemy import text


@bp.route('/api/cars', methods=['GET'])
def get_cars():
    sql = text('SELECT id, name, seat, door, body, displacement, car_length, wheelbase, power_type, brand, model, year, price FROM cars')
    result = db.session.execute(sql)

    cars_list = [dict(row._mapping) for row in result]

    return jsonify(cars_list)

@bp.route('/api/car/<int:id>')
def get_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    car_dict = dict(car._mapping)
    return jsonify(car_dict)