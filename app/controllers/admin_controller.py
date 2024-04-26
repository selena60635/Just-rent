import re
from app import db
from app.controllers import bp
from flask import render_template, request
from sqlalchemy import text

@bp.route('/admin')
def admin_index():
    return render_template('admin/index.html')

