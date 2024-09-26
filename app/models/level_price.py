from app import db

class LevelPrice(db.Model):
    __tablename__ = 'level_price'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    special_price = db.Column(db.Integer, nullable=False)


