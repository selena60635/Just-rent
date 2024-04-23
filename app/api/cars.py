from app import db
from app.api import bp
from flask import jsonify
from sqlalchemy import text


@bp.route('/api/cars', methods=['GET'])
def get_cars():
    sql = text('SELECT id, car_name, seat, door, body, displacement, car_length, wheelbase, power_type, brand, model FROM cars')
    result = db.session.execute(sql)

    cars_list = [dict(row._mapping) for row in result]

    return jsonify(cars_list)