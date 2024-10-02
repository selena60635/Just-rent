from flask_login import current_user
from app import db
from app.api import bp
from flask import jsonify, request
import re


@bp.route('/api/user/edit', methods=['POST'])
def edit_profile():
    user = current_user

    if not user:
        return jsonify({"message": "User not found"}), 401

    data = request.form

    # 驗證電話號碼格式
    phone_pattern = r"^09\d{8}$"
    if 'phone' in data and not re.match(phone_pattern, data['phone']):
        return jsonify({"message": "Invalid phone number. It must be 10 digits and start with 09."}), 400

    # 驗證密碼是否一致
    if 'user_password' in data and 'user_password_re-enter' in data:
        if data['user_password'] != data['user_password_re-enter']:
            return jsonify({"message": "Passwords do not match"}), 400

    # 更新使用者資料
    if 'username' in data:
        user.username = data['username']
    if 'email_address' in data:
        user.email = data['email_address']
    if 'phone' in data:
        user.phone = data['phone']
    if 'user_password' in data and data['user_password']:
        user.set_password(data['user_password']) 

    # 提交變更
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})
