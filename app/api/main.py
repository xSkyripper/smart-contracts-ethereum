import os
import json
from flask_cors import CORS
from sqlalchemy import exc
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
from flask_web3 import current_web3

from app import db, utils
from app.test.test_User import run_tests
from app.models import User, Contract, Role


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
    gov_id = request.form.get('gov_id')
    current_app.logger.info(f'Received PUT on user gov_id = {gov_id}')

    user = User.query.filter_by(gov_id=gov_id).first()
    if not user:
        user = User(registered=False)

    if not user.registered:
        if request.form.get('gov_id'):
            user.gov_id = request.form.get('gov_id')
        if request.form.get('first_name'):
            user.first_name = request.form.get('first_name')
        if request.form.get('last_name'):
            user.last_name = request.form.get('last_name')
        if request.form.get('email'):
            user.email = request.form.get('email')
        if request.form.get('ethereum_id'):
            user.ethereum_id = request.form.get('ethereum_id')
        if request.form.get('password'):
            user.password = request.form.get('password')
        user.registered = True

    try:
        if not user:
            db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(dict(error=f'There was an error updating the user with Id {gov_id}:{e.orig}')), 400

    return jsonify(dict(etag=gov_id, user=user.to_dict())), 204


@main_bp.route('/onboard', methods=['GET', 'POST'])
def onboard():
    contract_id = request.form.get('contract_id')
    gov_id = request.form.get('gov_id')
    user_ethereum_id = request.form.get('user_ethereum_id')

    current_app.logger.info(f'Received POST on onboard, contract_id {contract_id}, ssn {gov_id}, ethereum_id {user_ethereum_id}')

    if not all([contract_id, gov_id, user_ethereum_id]):
        return jsonify(dict(error=f'contract_id, gov_id and user_ethereum_id must be specified!')), 400

    user = User.query.filter_by(gov_id=gov_id).first()

    # Partially create user if it does not exist
    if not user:
        user = User(gov_id=gov_id, ethereum_id=user_ethereum_id)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError as e:
            current_app.logger.error(e.orig)
            db.session.rollback()
            return jsonify(dict(error=f'There was an error creating the user:{e.orig}')), 400
    # __end of partial creation

    if not contract_id:
        return jsonify(dict(error=f'contract_id must be specified!')), 400
    contract = Contract.query.get(contract_id)
    if not contract:
        return jsonify(dict(error=f"There is no contract with Id {contract_id}")), 404
    if user in contract.users:
        return jsonify(dict(error=f"The user with Id {user.id} is already in the contract {contract.id} users list")), 409

    try:
        contract.users.append(user)
        db.session.commit()
    except exc.IntegrityError as e: 
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(dict(error=f"There was an error adding user with Id {user_id} to contract with Id {contract_id}:{e.orig}")), 400

    cfg = current_app.config
    payment_contract = utils.get_payment_contract(cfg=current_app.config,
                                                  web3=current_web3,
                                                  contract_eth_addr=contract.ethereum_addr)

    try:
        eth_res = payment_contract.add_payer(user.ethereum_id)
    except ValueError as e:
        db.session.rollback()
        return jsonify(dict(error=f'Ethereum error!', 
                            ethereum_error=dict(message=eth_res['message']))), 400

    return jsonify(dict(etag=contract_id,
                        contract=contract.to_dict())), 204


@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return "logout"

@main_bp.route('/tests', methods=['GET'])
def tests():
    return str(run_tests())
