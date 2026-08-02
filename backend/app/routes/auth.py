from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app.constants.roles import UserRole
from app.constants.status import UserStatus
from app.extensions import db
from app.models import User
from app.utils.security import hash_password, verify_password

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/health")
def health():
    return {
        "message": "Authentication service is running."
    }


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    # Validate required fields
    if not all([name, email, password]):
        return jsonify({
            "error": "All required fields are mandatory."
        }), 400

    # Check duplicate email
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered."
        }), 409

    # Create user
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        phone=phone,
        role=UserRole.TREKKER.value
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful."
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if user.status != UserStatus.ACTIVE.value:
        return jsonify({
            "error": "Your account has been deactivated."
        }), 403

    if not user:
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    if not verify_password(password, user.password_hash):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found."
        }), 404

    return jsonify({
        "user": user.to_dict()
    }), 200