from app import db
import sqlalchemy.orm as so


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(255), nullable=False)
    hour_format = db.Column(db.String(255), nullable=False)


