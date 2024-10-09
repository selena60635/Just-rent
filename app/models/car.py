from app import db
import sqlalchemy.orm as so
from datetime import datetime, timezone


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default='Unknown')
    displacement = db.Column(db.Integer, nullable=False, default=0)
    body = db.Column(db.String(255), nullable=False, default='Unknown')
    seat = db.Column(db.Integer, nullable=False, default=0)
    door = db.Column(db.Integer, nullable=False, default=0)
    car_length = db.Column(db.Integer, nullable=False, default=0)
    wheelbase = db.Column(db.Integer, nullable=False, default=0)
    power_type = db.Column(db.String(255), nullable=False, default='Unknown')
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    year = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, db.ForeignKey("level_price.id"), nullable=False, default=1)
    level_price = db.relationship('LevelPrice', backref='cars')
    orders = db.relationship('Booking', back_populates='car')

    
