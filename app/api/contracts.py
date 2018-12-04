from datetime import datetime
from flask import request, current_app
from flask_restplus import Resource
from flask_login import current_user, login_required

from app.decorators import admin_required
from app.api.security import require_auth
from app.api import api_rest


@api_rest.route('/contracts/<int:contract_id>')
class Contract(Resource):
    def get(self, contract_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received GET on contract {contract_id}')
        return {
            'message': f'Called GET contract {contract_id}',
            'timestamp': timestamp,
            }

    def put(self, contract_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received PUT on contract {contract_id}')
        return {
            'message': f'Called PUT contract {contract_id}',
            'timestamp': timestamp,
            }

    def delete(self, contract_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received DELETE on contract {contract_id}')
        return {
            'message': f'Called DELETE contract {contract_id}',
            'timestamp': timestamp,
            }

@api_rest.route('/contracts')
class ContractList(Resource):
    def get(self):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received GET on contracts')
        return {
            'message': f'Called GET contract list',
            'timestamp': timestamp,
            }

    def post(self):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received POST on contracts')
        return {
            'message': f'Called POST contract list',
            'timestamp': timestamp,
            }, 201