from app import db
import sqlalchemy.orm as so
from datetime import datetime, timezone

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"))
    rent_location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    return_location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    pickup_date = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    return_date = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)
