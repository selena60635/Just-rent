from app import db
from app.api import bp
from flask import jsonify, current_app, url_for
from sqlalchemy import and_, or_, text
from flask import request

from app.models.car import Car

@bp.route('/api/cars', methods=['GET'])
def get_cars():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    body = request.args.get('body')
    seat = request.args.get('seat')
    engine = request.args.get('engine')
    max_price = request.args.get('max_price')
    # print(body,seat)

    conditions = []

    if body:
        bodies = body.split(',')
        body_condition = or_(*[Car.body == b for b in bodies])
        if 'other' in bodies:
            bodies.remove('other')
            other_bodies_condition = Car.body.notin_(['運動休旅車', '轎車', '雙門轎跑車', '掀背車', '休旅車'])
            body_condition = or_(other_bodies_condition, *[Car.body == b for b in bodies])
        conditions.append(body_condition)

    if seat:
        seats = seat.split(',')
        seat_condition = or_(*[Car.seat == s if s != '5plus' else Car.seat > 5 for s in seats])
        conditions.append(seat_condition)

    if engine:
        engine_ranges = engine.split(',')
        engine_condition = []
        for engine_range in engine_ranges:
            if engine_range == "1000~2000":
                engine_condition.append(Car.displacement.between(1000, 2000))
            elif engine_range == "2000~4000":
                engine_condition.append(Car.displacement.between(2000, 4000))
            elif engine_range == "4000~6000":
                engine_condition.append(Car.displacement.between(4000, 6000))
            elif engine_range == "6000plus":
                engine_condition.append(Car.displacement > 6000)
        conditions.append(or_(*engine_condition))


    if max_price:
        price_condition = Car.price.between(0, int(max_price))
        conditions.append(price_condition)

    query = db.session.query(Car)
    if conditions:
        query = query.where(*conditions)

    pagination = query.paginate(page=page, per_page=per_page)

    cars = pagination.items
    # print(query.statement.compile(compile_kwargs={"literal_binds": True}))
    response = {
        "cars": [{
            "id": car.id,
            "name": car.name,
            "brand": car.brand,
            "year": car.year,
            "model": car.model,
            "body": car.body,
            "displacement": car.displacement,
            "seat": car.seat,
            "door": car.door,
            "price": car.price
        } for car in cars],
        "has_next": pagination.has_next
    }

    # 以 JSON 格式回傳
    return jsonify(response)


@bp.route('/api/car/<int:id>')
def get_car(id):
    sql = text('SELECT * FROM cars WHERE id = :car_id')
    result = db.session.execute(sql, {'car_id': id})
    car = result.fetchone()
    car_dict = dict(car._mapping)
    return jsonify(car_dict)