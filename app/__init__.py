import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__, static_folder='../dist/static')

    config_cls = config[config_name]
    app.config.from_object(config_cls)
    app.url_map.strict_slashes = False
    
    # Modules init goes here
    config_cls.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    from app.security import setup_security
    setup_security()

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Blueprints registration goes here
    from app.main import main_bp
    from app.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app



