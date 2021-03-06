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


@api_rest.route('/contracts/<int:contract_id>')
class Contract(Resource):
    @user_required
    def get(self, contract_id):
        current_app.logger.info(f'Received GET on contract {contract_id}')
        contract = ContractModel.query.get(contract_id)
        
        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404
        
        cfg = current_app.config
        contract_data = contract.to_dict(with_users=True)
        contract_data['abi'] = utils.get_payment_contract_abi(cfg)
        
        return dict(contract=contract_data), 200

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
        
        payment_contract = utils.get_payment_contract(cfg=current_app.config,
                                                      web3=urrent_web3,
                                                      contract_eth_addr=contract.ethereum_addr)
        eth_res = payment_contract.close()

        db.session.delete(contract)

        return dict(), 204


@api_rest.route('/contracts')
class ContractList(Resource):
    @admin_required
    def get(self):
        current_app.logger.info(f'Received GET on contracts')
        contracts = ContractModel.query.all()
        
        cfg = current_app.config

        contracts_with_abi = []
        for contract in contracts:
            contract_data = contract.to_dict()
            contract_data['abi'] = utils.get_payment_contract_abi(cfg)
            contracts_with_abi.append(contract_data)

        return dict(contracts=contracts_with_abi), 200

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
            amount_due,
            owner=cfg['ETH_CONTRACT_OWNER'],
            contract_path=os.path.join(cfg['ETH_CONTRACTS_DIR'],
                                       cfg['ETH_CONTRACTS']['payment']['filename']),
            contract_name=cfg['ETH_CONTRACTS']['payment']['name'])

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


@api_rest.route('/contracts/<int:contract_id>/users')
class ContractUsersList(Resource):
    @admin_required
    def post(self, contract_id):
        current_app.logger.info(f'Received POST on ContractUsers contract {contract_id}')
        user_id = request.form.get('user_id')

        if not contract_id:
            return dict(error=f'contract_id must be specified!'), 400
        contract = ContractModel.query.get(contract_id)
        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404

        if not user_id:
            return dict(error=f"The user_id was not defined"), 400
        user = UserModel.query.get(user_id)
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404

        if user in contract.users:
            return dict(error=f"The user with Id {user.id} is already in the contract {contract.id} users list"), 409

        try:
            contract.users.append(user)
            db.session.commit()
        except exc.IntegrityError as e: 
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f"There was an error adding user with Id {user_id} to contract with Id {contract_id}:{e.orig}"), 400

        cfg = current_app.config
        payment_contract = utils.get_payment_contract(cfg=current_app.config,
                                                      web3=current_web3,
                                                      contract_eth_addr=contract.ethereum_addr)

        try:
            eth_res = payment_contract.add_payer(user.ethereum_id)
        except ValueError as e:
            db.session.rollback()
            return dict(error=f'Ethereum error!', 
                        ethereum_error=dict(message=eth_res['message'])), 400

        return dict(etag=contract_id,
                    contract=contract.to_dict()), 204
