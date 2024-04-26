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