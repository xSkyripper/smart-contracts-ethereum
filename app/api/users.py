from datetime import datetime
from flask import request, current_app
from flask_restplus import Resource
from flask_login import current_user, login_required

from app.models import User as UserModel
from app.decorators import admin_required
from app.api.security import require_auth
from app.api import api_rest
from app import db

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
        success = False

        # Get user json object from the request
        user_data_dict = request.form

        # Extract data from the request
        gov_id = user_data_dict['gov_id']
        first_name = user_data_dict['first_name']
        last_name = user_data_dict['last_name']
        email = user_data_dict['email']
        ethereum_id = user_data_dict['ethereum_id']
        password_hash = user_data_dict['password_hash']
        role_id = user_data_dict['role_id']
        contracts = user_data_dict['contracts']
        
        # Get user object from the users (UserModel) table
        user = UserModel.query.get(user_id)
        
        # Update User data, if present in the request
        if gov_id and len(gov_id) > 0:
            user.gov_id = gov_id
        if first_name and len(first_name) > 0:
            user.first_name = first_name
        if last_name and len(last_name) > 0:
            user.last_name = last_name
        if email and len(email) > 0:
            user.email = email
        if ethereum_id and len(ethereum_id) > 0:
            user.ethereum_id = ethereum_id
        if password_hash and len(password_hash) > 0:
            user.password_hash = etherepassword_hashum_id
        if contracts and len(contracts) > 0:
            user.contracts = contracts
        if role_id and len(role_id) > 0:
            user.role_id = role_id

        current_app.logger.info(f'Trying to add user: {user}')

        try:
            db.session.commit()
            success = True
        except IntegrityError:
            db.session.rollback()

        if success:
            message = f'Successfully added user to the database. User: {user}'
        else:
            message = f'Failed to add user to the database. User: {user}'
        
        return {
            'message': message,
            'timestamp': timestamp,
            }

    # @admin_required
    def delete(self, user_id):
        timestamp = datetime.utcnow().isoformat()
        current_app.logger.info(f'Received DELETE on user {user_id}')
        # db.session.delete()
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