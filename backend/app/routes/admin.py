from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.admin_service import AdminService
from app.utils.decorators import admin_required

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
def dashboard():

    return jsonify(
        AdminService.get_dashboard_statistics()
    ), 200


@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
@admin_required
def create_trek():

    try:
        trek = AdminService.create_trek(request.get_json())

        return jsonify({
            "message": "Trek created successfully.",
            "trek": trek.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
@admin_required
def get_all_treks():

    treks = AdminService.get_all_treks()

    return jsonify({
        "treks": [
            trek.to_dict()
            for trek in treks
        ]
    }), 200

@admin_bp.route("/treks/<int:trek_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_trek(trek_id):

    try:

        trek = AdminService.get_trek(trek_id)

        return jsonify({
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_trek(trek_id):

    try:

        trek = AdminService.update_trek(
            trek_id,
            request.get_json()
        )

        return jsonify({
            "message": "Trek updated successfully.",
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_trek(trek_id):

    try:

        AdminService.delete_trek(trek_id)

        return jsonify({
            "message": "Trek deleted successfully."
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@admin_bp.route("/staff", methods=["POST"])
@jwt_required()
@admin_required
def create_staff():

    try:

        user = AdminService.create_staff(
            request.get_json()
        )

        return jsonify({
            "message": "Staff created successfully.",
            "staff": user.to_dict()
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@admin_bp.route("/staff", methods=["GET"])
@jwt_required()
@admin_required
def get_all_staff():

    staff = AdminService.get_all_staff()

    return jsonify({
        "staff": [
            member.to_dict()
            for member in staff
        ]
    }), 200

@admin_bp.route("/staff/<int:staff_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_staff(staff_id):

    try:

        staff = AdminService.get_staff(staff_id)

        return jsonify({
            "staff": staff.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_staff(staff_id):

    try:

        staff = AdminService.update_staff(
            staff_id,
            request.get_json()
        )

        return jsonify({
            "message": "Staff updated successfully.",
            "staff": staff.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


@admin_bp.route("/staff/<int:staff_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_staff(staff_id):

    try:

        AdminService.delete_staff(staff_id)

        return jsonify({
            "message": "Staff deleted successfully."
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


@admin_bp.route("/treks/<int:trek_id>/assign", methods=["PUT"])
@jwt_required()
@admin_required
def assign_staff(trek_id):

    data = request.get_json()

    try:

        trek = AdminService.assign_staff(
            trek_id,
            data.get("staff_id")
        )

        return jsonify({
            "message": "Staff assigned successfully.",
            "trek": trek.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():

    users = AdminService.get_all_users()

    return jsonify({
        "users": [
            user.to_dict()
            for user in users
        ]
    }), 200

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user(user_id):

    try:

        user = AdminService.get_user(user_id)

        return jsonify({
            "user": user.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def update_user_status(user_id):

    data = request.get_json()

    try:

        current_admin_id = int(get_jwt_identity())

        user = AdminService.update_user_status(
            user_id,
            data.get("status"),
            current_admin_id
        )

        return jsonify({
            "message": "User status updated successfully.",
            "user": user.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


@admin_bp.route("/search", methods=["GET"])
@jwt_required()
@admin_required
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required."
        }), 400

    result = AdminService.search(query)

    return jsonify(result), 200

