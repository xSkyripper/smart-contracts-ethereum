from datetime import datetime
from flask import request, current_app
from flask_restplus import Resource
from sqlalchemy import exc

from app.models import User as UserModel
from app.security import admin_required, user_required
from app.api import api_rest
from app import db


@api_rest.route('/users/<int:user_id>')
class User(Resource):
    @admin_required
    def get(self, user_id):
        current_app.logger.info(f'Received GET on user {user_id}')
        user = UserModel.query.get(user_id)
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404
        return dict(user=user.to_dict()), 200

    @user_required
    def put(self, user_id):
        current_app.logger.info(f'Received PUT on user {user_id}')

        # Get user json object from the request
        user_data_dict = request.form

        # Get user object from the users (UserModel) table
        user = UserModel.query.get(user_id)
        
        # Stop if the user does not exist
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404
        
        # Update User data, if present in the request
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
        if request.form.get('password_hash'):
            user.password_hash = request.form.get('password_hash')
        if request.form.get('contracts'):
            user.contracts = request.form.get('contracts')
        if request.form.get('role_id'):
            user.role_id = request.form.get('role_id')

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return dict(error=f'There was an error updating the user with Id {user_id}:{e.orig}'), 400

        return dict(etag=user_id, user=user.to_dict()), 204

    @admin_required
    def delete(self, user_id):
        current_app.logger.info(f'Received DELETE on user {user_id}')
        
        # Get user with specified id
        user = UserModel.query.get(user_id)
        
        # Stop if the user does not exist
        if not user:
            return dict(error=f"There is no user with Id {user_id}"), 404
        
        # Delete user
        db.session.delete(user)

        return dict(), 204


@api_rest.route('/users')
class UserList(Resource):
    @user_required
    def get(self):
        current_app.logger.info(f'Received GET on users')

        users = UserModel.query.all()

        return dict(users=[user.to_dict() for user in users]), 200

    @admin_required
    def post(self):
        current_app.logger.info(f'Received POST on users')
        
        gov_id = request.form.get('gov_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        ethereum_id = request.form.get('ethereum_id')
        password_hash = (request.form.get('password') or '') + 'hashed'
        role_id = request.form.get('role_id')

        user = UserModel(gov_id=gov_id,
                         first_name=first_name,
                         last_name=last_name,
                         email=email,
                         ethereum_id=ethereum_id,
                         password_hash=password_hash,
                         role_id=role_id)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError as e:
            current_app.logger.error(e.orig)
            db.session.rollback()
            return dict(error=f'There was an error creating the user:{e.orig}'), 400

        return dict(user=user.to_dict()), 201


@api_rest.route('/users/<int:user_id>/contracts')
class UserContractsList(Resource):
    # TODO: HARDCODED
    def get(self, user_id):
        return dict(contracts=[{
                "id": 1,
                "amount_due": 69,
                "name": "Test1Contract",
                "description": "PWxjaFAPHmnmzqfHsSuhJHDfgQnGVeissiJeUyTjZVCPdtGrTMXbow",
                "ethereum_addr": "VhtMtETeFvucWSenfGXrHVrkZnieUqXvTpqcAmsC",
                "abi": "cTxsmyXGqPMWAmWslweUqimgORrdRYOVpVoRpIgiZNtOmIBqymUTjTbJAZTAWALtNwjZkhKaABgdvjvCdulzdXPCqpTIeSHOHcZddHIc",
                "users": []}])