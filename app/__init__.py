import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.config import config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main_bp.login'


def create_app(config_name):
    app = Flask(__name__, static_folder='../dist/static')

    config_cls = config[config_name]
    app.config.from_object(config_cls)
    
    # Modules init goes here
    config_cls.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Blueprints registration goes here
    from app.main import main_bp
    from app.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    app.logger.info('>>> {}'.format(config_cls.FLASK_ENV))
    return app



