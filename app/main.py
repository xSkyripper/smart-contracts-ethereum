import os
from flask_cors import CORS
import json
from app.test.test_User import run_tests

from flask import (
    Blueprint,
    render_template,
    current_app,
    send_file,
    request,
    jsonify,
    )
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash


from app.models import User


main_bp = Blueprint('main_bp', __name__,
                    url_prefix='',
                    static_url_path='',
                    static_folder='./dist/static/',
                    template_folder='./dist/',
                    )

CORS(main_bp, resources={r"*": {"origins": "*"}})

@main_bp.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify(dict(error=f"Invalid parameters")), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify(dict(error=f"Invalid email or password")), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify(dict(error=f'Invalid email or password')), 401 

    access_token = create_access_token(identity=user.id)

    return jsonify(dict(access_token=access_token)), 200

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    return "register"

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return "logout"

@main_bp.route('/tests', methods=['GET'])
def tests():
    return str(run_tests())
