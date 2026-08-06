from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.services.staff_service import StaffService
from app.utils.decorators import staff_required

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/api/staff"
)

@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@staff_required
def dashboard():

    user_id = int(get_jwt_identity())

    return jsonify(
        StaffService.get_dashboard(user_id)
    ), 200

@staff_bp.route("/treks", methods=["GET"])
@jwt_required()
@staff_required
def get_assigned_treks():

    user_id = int(get_jwt_identity())

    treks = StaffService.get_assigned_treks(user_id)

    return jsonify({
        "treks": treks
    }), 200

@staff_bp.route("/treks/<int:trek_id>", methods=["GET"])
@jwt_required()
@staff_required
def get_trek_details(trek_id):

    user_id = int(get_jwt_identity())

    try:

        trek = StaffService.get_trek_details(
            user_id,
            trek_id
        )

        return jsonify({
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
@staff_required
def get_participants(trek_id):

    user_id = int(get_jwt_identity())

    try:

        participants = StaffService.get_participants(
            user_id,
            trek_id
        )

        return jsonify({
            "participants": participants
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
@staff_required
def update_trek_status(trek_id):

    user_id = int(get_jwt_identity())

    data = request.get_json()

    try:

        trek = StaffService.update_trek_status(
            user_id,
            trek_id,
            data.get("status")
        )

        return jsonify({
            "message": "Status updated successfully.",
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@staff_bp.route("/treks/<int:trek_id>/complete", methods=["PUT"])
@jwt_required()
@staff_required
def complete_trek(trek_id):

    user_id = int(get_jwt_identity())

    try:

        trek = StaffService.complete_trek(
            user_id,
            trek_id
        )

        return jsonify({
            "message": "Trek marked as completed.",
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400