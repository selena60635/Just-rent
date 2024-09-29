from app import db
import sqlalchemy.orm as so
from datetime import datetime, timezone

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    pickup_time = db.Column(db.Time, index=True, nullable=False)
    return_time = db.Column(db.Time, index=True, nullable=False) 
    pick_up_loc= db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    drop_off_loc = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    total_price = db.Column(db.Integer, nullable=False, default=0) 
    status = db.Column(db.String(255), nullable=False, default='Pending')
    car = db.relationship('Car', back_populates='orders')
    user = db.relationship('User', backref='booking')
    pickup_location = db.relationship('Location', foreign_keys=[pick_up_loc])
    return_location = db.relationship('Location', foreign_keys=[drop_off_loc])
