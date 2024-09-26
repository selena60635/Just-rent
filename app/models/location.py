from app import db
from sqlalchemy import DECIMAL

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(DECIMAL(18, 15), nullable=True) 
    longitude = db.Column(DECIMAL(18, 15), nullable=True)
