from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.controllers import bp as controllers_bp
    app.register_blueprint(controllers_bp)

    from app.error import bp as error_bp
    app.register_blueprint(error_bp)
    
    return app

