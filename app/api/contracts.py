import os.path

from sqlalchemy import exc
from flask import request, current_app, jsonify
from flask_restplus import Resource
from flask_web3 import current_web3

from app import db
from app import utils
from app.api import api_rest
from app.models import Contract as ContractModel, User as UserModel
from app.security import admin_required, user_required
from app.ethereum import Manager as SCManager, PaymentContract

@api_rest.route('/contracts/<int:contract_id>/users')
class ContractUsersList(Resource):
    @admin_required
    def post(self, contract_id):
        current_app.logger.info(f'Received POST on ContractUsers contract {contract_id}')
        contract = ContractModel.query.get(contract_id)

        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404

        if not request.form.get('user_id'):
            return dict(error=f"Bad request: the user_id was not defined"), 400

        user_id = request.form.get('user_id')
        user = UserModel.query.get(user_id)

        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404

        try:
            contract.users.append(user)
            db.session.commit()
        except exc.IntegrityError as e: 
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error adding user with Id {user_id} to contract with Id {contract_id}:{e.orig}'), 400
        
        # TODO: call SCManager to add user

        return dict(etag=contract_id, contract=contract.to_dict(with_users=True)), 200

    # TODO: implement delete user from contract


@api_rest.route('/contracts/<int:contract_id>')
class Contract(Resource):
    @user_required
    def get(self, contract_id):
        current_app.logger.info(f'Received GET on contract {contract_id}')
        contract = ContractModel.query.get(contract_id)
        
        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404
        
        return dict(contract=contract.to_dict()), 200
        # return dict(contracts=[{"id": 7, "name": "name1", "service": "service1"}]), 201

    @admin_required
    def put(self, contract_id):
        current_app.logger.info(f'Received PUT on contract {contract_id}')

        contract = ContractModel.query.get(contract_id)

        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404

        if request.form.get('name'):
            contract.name = request.form.get('name')
        
        if request.form.get('amount_due'):
            contract.amount_due = request.form.get('amount_due')

        if request.form.get('description'):
            contract.description = request.form.get('description')
        
        if request.form.get('ethereum_addr'):
            contract.ethereum_addr = request.form.get('ethereum_addr')

        if request.form.get('user_ids'):
            user_ids_csv = request.form.get('user_ids')
            user_ids = user_ids_csv.strip().split(',')
            current_app.logger.info(f'Received list of user_ids {user_ids} for PUT on contract {contract_id}')

            users = []
            for user_id in user_ids:
                user = UserModel.query.get(user_id)
                users.append(user)
            contract.users = users

        try:
            db.session.commit()
        except exc.IntegrityError as e: 
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error updating the contract with Id {contract_id}:{e.orig}'), 400
        
        return dict(etag=contract_id, contract=contract.to_dict()), 200

    @admin_required
    def delete(self, contract_id):
        current_app.logger.info(f'Received DELETE on contract {contract_id}')

        contract = ContractModel.query.get(contract_id)

        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404
        
        pc = utils.get_payment_contract(current_app.config, current_web3, contract.ethereum_addr)
        eth_res = pc.close()

        db.session.delete(contract)

        return dict(), 204

@api_rest.route('/contracts')
class ContractList(Resource):
    @admin_required
    def get(self):
        current_app.logger.info(f'Received GET on contracts')
        contracts = ContractModel.query.all()
        return dict(contracts=[contract.to_dict() for contract in contracts]), 200

    @admin_required
    def post(self):
        current_app.logger.info(f'Received POST on contracts')

        name = request.form.get('name')
        description = request.form.get('description')
        amount_due = request.form.get('amount_due')

        if not amount_due:
            return dict(error=f'amount_due must be specified'), 400
        amount_due = int(amount_due)

        scm = SCManager(current_web3)
        # 1000000000000000000 = 1 ether
        cfg = current_app.config
        contract_eth_addr = scm.create_contract(
            cfg['ETH_CONTRACT_OWNER'],
            os.path.join(cfg['ETH_CONTRACTS_DIR'], cfg['ETH_CONTRACTS']['payment']['filename']),
            cfg['ETH_CONTRACTS']['payment']['name'],
            amount_due)

        contract = ContractModel(amount_due=amount_due,
                                 name=name,
                                 description=description,
                                 ethereum_addr=contract_eth_addr)

        try:
            db.session.add(contract)
            db.session.commit()
        except exc.IntegrityError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error creating the contract:{e.orig}'), 400

        return dict(contract=contract.to_dict()), 201