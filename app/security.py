from functools import wraps
from flask import abort, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, current_user, verify_jwt_in_request
)
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.models.user import Permission, User


def setup_security():
    from app import jwt

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        user = User.query.get(identity)
        if not user:
            return None
        return user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        return dict(msg=f"User {identity} not found"), 404


def permission_required(permission):
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if not request.headers.get('Authorization'):
            #     return jsonify(dict(error=f"Missing authorization header"), 403)
                
            # verify_jwt_in_request()

            # if not current_user.can(permission):
            #     return jsonify(dict(error=f"Unauthorized to do this"), 403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def user_required(f):
    return permission_required(Permission.USER)(f)


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

