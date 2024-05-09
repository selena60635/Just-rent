from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'controller.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.controllers import bp as controllers_bp
    app.register_blueprint(controllers_bp)

    from app.error import bp as error_bp
    app.register_blueprint(error_bp)

    from app.models import bp as models_bp
    app.register_blueprint(models_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

