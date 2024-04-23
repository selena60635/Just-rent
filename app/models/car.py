from app import db
from app.models.user import User
import sqlalchemy.orm as so
from datetime import datetime, timezone

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(255), nullable=False, default='Unknown')
    displacement = db.Column(db.Integer, nullable=False, default=0)
    body = db.Column(db.String(255), nullable=False, default='Unknown')
    seat = db.Column(db.Integer, nullable=False, default=0)
    door = db.Column(db.Integer, nullable=False, default=0)
    car_length = db.Column(db.Integer, nullable=False, default=0)
    wheelbase = db.Column(db.Integer, nullable=False, default=0)
    power_type = db.Column(db.String(255), nullable=False, default='Unknown')
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    available_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    last_return_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    like_users = db.Column(db.Integer, db.ForeignKey('users.id'))

    
