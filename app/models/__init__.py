from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('models', __name__)

from app.models.user import User
from app.models.car import Car
from app.models.booking import Booking
from app.models.location import Location
from app.models.level_price import LevelPrice
