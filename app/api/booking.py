from app import db
from app.api import bp
from flask import jsonify, request,redirect
from app.models.location import Location 
from flask_login import current_user
from functools import wraps
from datetime import datetime, timezone
from app.models import Booking
import tappay
import os
from dotenv import load_dotenv


def login_required_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'status': 'noauth'})
        return f(*args, **kwargs)
    return decorated_function

# 取得位置資訊
@bp.route('/api/booking/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    location_names = [location.name for location in locations]
    return jsonify(location_names)

# 新增一筆booking資料(訂單)
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

    # 檢查是否已有該使用者的未完成訂單，限制一位使用者只能一次租用一台車
    # existing_booking_user = Booking.query.filter_by(user_id=user_id, car_id=car_id, status='pending').first()
    # if existing_booking_user:
    #     return jsonify({"error": "您已經有一筆未完成的訂單，無法再次租用此車輛。"})


    pickup_datetime = datetime.strptime(f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M")
    return_datetime = datetime.strptime(f"{return_date} {return_time}", "%Y-%m-%d %H:%M")

    # 檢查該汽車的該時段是否已被租用
    is_booking = Booking.query.filter(
        Booking.car_id == car_id,
        (Booking.pickup_date <= return_datetime) & (Booking.return_date >= pickup_datetime)
    ).first()

    if is_booking:
        return jsonify({"error": "The vehicle has already been rented during this time period."})
    
    # 計算總時數
    total_hours = (return_datetime - pickup_datetime).total_seconds() / 3600
    # 計算總價
    total_price = int(price) * total_hours
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
        total_price=total_price,
        status='pending'
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
        "userEmail": new_booking.user.email,  
        "userPhone": new_booking.user.phone,
        "created_at": new_booking.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_date": new_booking.pickup_date.strftime("%Y-%m-%d"),
        "return_date": new_booking.return_date.strftime("%Y-%m-%d"),
        "pickup_time": new_booking.pickup_time.strftime("%H:%M:%S"),
        "return_time": new_booking.return_time.strftime("%H:%M:%S"),
        "pickup_loc": pickup_loc,
        "return_loc": return_loc,
        "total_price": total_price,
        "total_hours":total_hours,
        "status": new_booking.status
    }

    return jsonify(response_data), 201

#取消並刪除訂單
@bp.route('/api/booking/cancel_order/<int:orderId>', methods=['POST'])
def cancel_order(orderId):
    order = Booking.query.get(orderId)
    if not order:
        return jsonify({"error": "Order not found."})
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order canceled."})

@bp.route('/api/bookings', methods=['GET'])
def get_orders():
        bookings = Booking.query.filter_by(user_id=current_user.id).all() 
        bookings_data = [
            {
                'id': booking.id,
                'car_name': booking.car.name,
                'pickup_location': booking.pickup_location.name,
                'return_location': booking.return_location.name,
                'pickup_date': booking.pickup_date.strftime('%Y-%m-%d'),
                'pickup_time': booking.pickup_time.strftime('%H:%M:%S'),
                'return_date': booking.return_date.strftime('%Y-%m-%d'),
                'return_time': booking.return_time.strftime('%H:%M:%S'),
                'status': booking.status 
            }
            for booking in bookings
        ]
        return jsonify(bookings_data) 




#處理付款
load_dotenv()
partner_key = os.getenv('PARTNER_KEY')
merchant_id = os.getenv('MERCHANT_ID')

client = tappay.Client(True, partner_key, merchant_id)
@bp.route('/api/booking/payment', methods=['POST'])
def process_payment():
    data = request.json
    prime = data.get('prime')
    amount = data.get('amount')
    booking_id = data.get('booking_id')
    user_name = current_user.username
    user_email = current_user.email
    phone_number = current_user.phone

    # 檢查是否取得必要的參數
    if not prime or not amount or not user_name or not user_email or not phone_number:
        return jsonify({'message': 'Please provide the required payment information.'}), 400
     # 檢查是否已付款
    booking = Booking.query.get(booking_id)
    if not booking or booking.status == 'scheduled':

        return jsonify({
            'message':"Invalid order or this order has already been paid, please do not make duplicate payments."
        }), 400

    # 建立付款的卡片持有人資料
    card_holder_data = tappay.Models.CardHolderData(
        phone_number=phone_number, 
        name=user_name,
        email=user_email
    )

    try:
        response_data = client.pay_by_prime(
            prime=prime,
            amount=amount,
            details='Car Rental Payment',
            card_holder_data=card_holder_data
        )

    except Exception as e:
        # import traceback
        # print("Error:", traceback.format_exc()) 
        return jsonify({'error': str(e)}), 500

    # status=0表示付款成功
    if response_data['status'] == 0:
        # 更新訂單為已付款狀態
        booking.status = "scheduled"  
        db.session.commit()

        return jsonify({
            'message': 'Payment successful',
            'transaction_id': response_data['rec_trade_id']
        }), 200
    else:
        return jsonify({
            'error': 'Payment failed',
            'message': response_data.get('msg', 'Unknown error')
        }), 400


