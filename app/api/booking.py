from app import db
from app.api import bp
from flask import jsonify, request
from app.models.location import Location 
from flask_login import current_user
from functools import wraps
from datetime import datetime, timezone
from app.models import Booking


def login_required_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'status': 'noauth'})
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/api/booking/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    location_names = [location.name for location in locations]
    return jsonify(location_names)


@bp.route('/api/booking/order', methods=['POST'])
@login_required_auth
def add_order():
    user_id = current_user.id 
    car_id = request.form.get('car-id-input')
    price = request.form.get('car-price-input')
    pickup_loc = request.form.get('pickupLoc')
    return_loc = request.form.get('dropoffLoc')
    pickup_date = request.form.get('pickup-date')
    return_date = request.form.get('return-date')
    pickup_time = request.form.get('pickup-time')
    return_time = request.form.get('return-time')

    pickup_location = Location.query.filter_by(name=pickup_loc).first()
    return_location = Location.query.filter_by(name=return_loc).first()

    # 檢查是否已有該使用者的未完成訂單
    # existing_booking_user = Booking.query.filter_by(user_id=user_id, car_id=car_id, status='Pending').first()
    # if existing_booking_user:
    #     return jsonify({"error": "您已經有一筆未完成的訂單，無法再次租用此車輛。"})

    # 檢查是否該車已被其他人租用
    # existing_booking_car = Booking.query.filter_by(car_id=car_id, status='Pending').first()
    # if existing_booking_car:
    #     return jsonify({"error": "該車輛已被其他人租用，無法再次建立訂單。"})
    pickup_datetime = datetime.strptime(f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M")
    return_datetime = datetime.strptime(f"{return_date} {return_time}", "%Y-%m-%d %H:%M")

    # 檢查是否該車已被其他人租用，且租用時間有重疊
    overlapping_booking = Booking.query.filter(
        Booking.car_id == car_id,
        (Booking.pickup_date <= return_datetime) & (Booking.return_date >= pickup_datetime)
    ).first()

    if overlapping_booking:
        return jsonify({"error": "該車輛在此時間段內已被租用，無法再次建立訂單。"})
    

    # duration_hours = (return_datetime - pickup_datetime).total_seconds() / 3600
    # total_price = price * duration_hours

    # 建立新的訂單
    new_booking = Booking(
        user_id=user_id,
        car_id=car_id,
        created_at=datetime.now(timezone.utc),
        pickup_date=pickup_date,
        return_date=return_date,
        pickup_time=pickup_time,
        return_time=return_time,
        pick_up_loc=pickup_location.id,
        drop_off_loc=return_location.id,
        status='Pending'
    )

    # 新增資料到資料庫
    db.session.add(new_booking)
    db.session.commit()

    response_data = {
        "bookingId": new_booking.id,
        "carId": new_booking.car_id,
        "carName": new_booking.car.name,
        "userId": new_booking.user_id,
        "userName": new_booking.user.username,
        "created_at": new_booking.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_date": new_booking.pickup_date.strftime("%Y-%m-%d"),
        "return_date": new_booking.return_date.strftime("%Y-%m-%d"),
        "pickup_time": new_booking.pickup_time.strftime("%H:%M:%S"),
        "return_time": new_booking.return_time.strftime("%H:%M:%S"),
        "pickup_loc": pickup_loc,
        "return_loc": return_loc,
        "price": price,
        "status": new_booking.status
    }

    return jsonify(response_data), 201

@bp.route('/api/booking/cancel_order/<int:orderId>', methods=['POST'])
def cancel_order(orderId):
    # print(orderId)
    order = Booking.query.get(orderId)
    if not order:
        return jsonify({"error": "找不到該筆訂單"})
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "已取消訂單"})


