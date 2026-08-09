from flask import Blueprint, jsonify, request, send_file
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.admin_service import AdminService
from app.utils.decorators import admin_required
from app.utils.validators import validate_trek_data, validate_staff_data
from app.extensions import cache

from app.tasks.reports import monthly_report

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
@cache.cached(timeout=300)
def dashboard():

    return jsonify(
        AdminService.get_dashboard_statistics()
    ), 200


@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
@admin_required
def create_trek():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        error = validate_trek_data(data)

        if error:
            return jsonify({
                "error": error
            }), 400

        trek = AdminService.create_trek(data)

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

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        trek = AdminService.update_trek(
            trek_id,
            data
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

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        error = validate_staff_data(data)

        if error:
            return jsonify({
                "error": error
            }), 400

        user = AdminService.create_staff(data)

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

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be valid JSON."
            }), 400

        staff = AdminService.update_staff(
            staff_id,
            data
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

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

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

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

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

@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def get_all_bookings():

    bookings = AdminService.get_all_bookings()

    return jsonify({
        "bookings": [
            {
                **booking.to_dict(),
                "user": booking.user.to_dict(),
                "trek": booking.trek.to_dict()
            }
            for booking in bookings
        ]
    }), 200

@admin_bp.route("/history", methods=["GET"])
@jwt_required()
@admin_required
def get_trek_history():

    history = AdminService.get_trek_history()

    return jsonify({
        "history": [
            trek.to_dict()
            for trek in history
        ]
    }), 200

@admin_bp.route("/report/generate", methods=["POST"])
@jwt_required()
@admin_required
def generate_report():
    """Generate monthly report synchronously and return its path."""
    from app.services.report_service import ReportService
    filename = ReportService.generate_monthly_report()
    return jsonify({
        "message": "Report generated successfully.",
        "filename": filename
    }), 200

@admin_bp.route("/report/download", methods=["GET"])
@jwt_required()
@admin_required
def download_report():
    """Download the most recently generated monthly report."""
    filepath = os.path.join("reports", "monthly_report.html")
    if not os.path.exists(filepath):
        return jsonify({
            "error": "No report found. Please generate it first."
        }), 404
    return send_file(
        os.path.abspath(filepath),
        mimetype="text/html",
        as_attachment=False
    )