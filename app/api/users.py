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

        # Get user object from the users (UserModel) table
        user = UserModel.query.get(user_id)
        
        # Stop if the user does not exist
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404
        
        # Update User data, if present in the request
        if request.form.get('gov_id'):
            user.gov_id = gov_id
        if request.form.get('first_name'):
            user.first_name = first_name
        if request.form.get('last_name'):
            user.last_name = last_name
        if request.form.get('email'):
            user.email = email
        if request.form.get('ethereum_id'):
            user.ethereum_id = ethereum_id
        if request.form.get('password_hash'):
            user.password_hash = password_hash
        if request.form.get('contracts'):
            user.contracts = contracts
        if request.form.get('role_id'):
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
        
        # Get user with specified id
        user = UserModel.query.get(user_id)
        
        # Stop if the user does not exist
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404
        
        # Delete user
        db.session.delete(user)

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