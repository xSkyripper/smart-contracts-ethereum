from datetime import datetime
from flask import request, current_app
from flask_restplus import Resource
from flask_login import current_user, login_required

from app.models import User as UserModel
from app.decorators import admin_required
from app.api.security import require_auth
from app.api import api_rest
ns = api_rest.namespace('users', description='Users RESTful API')

@ns.route('/<int:user_id>')
class User(Resource):
    # method_decorators = [login_required]
    # TODO: decorate each route for each resource based on requirements (login_required, admin_required)

    # @login_required
    def get(self, user_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received GET on user {user_id}')

        user = UserModel.query.get(user_id)

        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404

        return dict(
            user=dict(
                id=user.id,
                gov_id=user.gov_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                ethereum_id=user.ethereum_id)), 200

    # @login_required
    def put(self, user_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received PUT on user {user_id}')
        return {
            'message': f'Called PUT user {user_id}',
            'timestamp': timestamp,
            }

    # @admin_required
    def delete(self, user_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received DELETE on user {user_id}')
        return {
            'message': f'Called DELETE user {user_id}',
            'timestamp': timestamp,
            }

@ns.route('/')
class UserList(Resource):
    def get(self):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received GET on users')
        return {
            'message': f'Called GET user list',
            'timestamp': timestamp,
            }

    def post(self):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received POST on users')
        return {
            'message': f'Called POST user list',
            'timestamp': timestamp,
            }, 201