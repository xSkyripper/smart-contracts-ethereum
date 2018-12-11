from datetime import datetime
from flask import request, current_app
from flask_restplus import Resource
from flask_login import current_user, login_required

from app import db
from app.models import Contract as ContractModel
from app.decorators import admin_required
from app.api.security import require_auth
from app.api import api_rest
from pprint import pprint


@api_rest.route('/contracts/<int:contract_id>')
class Contract(Resource):
    # @login_required
    def get(self, contract_id):
        current_app.logger.info(f'Received GET on contract {contract_id}')
        contract = ContractModel.query.get(contract_id)
        
        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404
        
        return dict(contract=contract.to_dict()), 200

    # @login_required
    def put(self, contract_id):
        current_app.logger.info(f'Received PUT on contract {contract_id}')
        success = False

        contract = ContractModel.query.get(contract_id)

        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404

        if request.form.get('type'):
            contract.type = request.form.get('type')
        
        if request.form.get('tax'):
            contract.tax = request.form.get('tax')

        if request.form.get('description'):
            contract.description = request.form.get('description')
        
        if request.form.get('ethereum_addr'):
            contract.ethereum_addr = request.form.get('ethereum_addr')

        try:
            db.session.commit()
        except IntegrityError as e: 
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error updating the contract with Id {contract_id}:{e.message}'), 400
        
        return dict(etag=contract_id, contract=contract.to_dict()), 204

    # @login_required
    def delete(self, contract_id):
        current_app.logger.info(f'Received DELETE on contract {contract_id}')

        contract = ContractModel.query.get(contract_id)

        if not contract:
            return dict(error=f"There is no contract with Id {contract_id}"), 404

        db.session.delete(contract)

        return dict(), 204

@api_rest.route('/contracts')
class ContractList(Resource):
    def get(self):
        current_app.logger.info(f'Received GET on contracts')

        contracts = ContractModel.query.all()

        return dict(contracts=[contract.to_dict() for contract in contracts]), 200

    def post(self):
        current_app.logger.info(f'Received POST on contracts')

        tax = request.form.get('tax')
        contract_type = request.form.get('type')
        description = request.form.get('description')
        ethereum_addr = 'some eth addr'

        # TODO: create the contract in Ethereum

        contract = ContractModel(tax=tax,
                                 type=contract_type,
                                 description=description,
                                 ethereum_addr=ethereum_addr)

        try:
            db.session.add(contract)
            db.session.commit()
        except IntegrityErrror as e:
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error creating the contract:{e.message}'), 400

        return dict(contract=contract.to_dict()), 201