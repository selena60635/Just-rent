from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, default="0912345678")
    language = db.Column(db.String(255), nullable=False, default='English')
    hour_format = db.Column(db.String(255), nullable=False, default='24-hour')
    role = db.Column(db.String(255), nullable=False, default='basic')

    liked_cars = db.relationship('Car', secondary=likes,backref=db.backref('liked_by', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={128}'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

