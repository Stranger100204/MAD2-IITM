from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt

from app.constants.roles import UserRole


def role_required(required_role):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role != required_role:
                return jsonify({
                    "error": "You do not have permission to access this resource."
                }), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required(UserRole.ADMIN.value)
staff_required = role_required(UserRole.STAFF.value)
trekker_required = role_required(UserRole.TREKKER.value)