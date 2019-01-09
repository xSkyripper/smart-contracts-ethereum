""" API Blueprint Application """

from flask import Blueprint, current_app
from flask_restplus import Api
from flask_cors import CORS

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)

CORS(api_bp, resources={r"/*": {"origins": "*"}})

@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# Import resources to ensure view is registered
from app.api.resources import * # NOQA
from app.api.users import *
from app.api.contracts import *