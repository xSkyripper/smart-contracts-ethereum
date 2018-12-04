import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../dist/static')

    from app.config import Config
    app.config.from_object('app.config.Config')

    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app
    # from app.client import client_bp
    # app.register_blueprint(client_bp)



