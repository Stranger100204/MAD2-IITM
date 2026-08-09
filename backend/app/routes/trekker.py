from flask import Blueprint, jsonify, send_file
from flask import request
import os

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.utils.decorators import trekker_required
from app.services.trekker_service import TrekkerService
from app.extensions import cache
from app.tasks.exports import export_booking_history
from app.tasks.reminders import daily_reminder

trekker_bp = Blueprint(
    "trekker",
    __name__,
    url_prefix="/api/trekker"
)


@trekker_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@trekker_required
@cache.cached(timeout=300)
def dashboard():

    user_id = int(get_jwt_identity())

    return jsonify(
        TrekkerService.get_dashboard(user_id)
    ), 200

@trekker_bp.route("/treks", methods=["GET"])
@jwt_required()
@trekker_required
@cache.cached(timeout=300)
def get_available_treks():

    treks = TrekkerService.get_available_treks()

    return jsonify({
        "treks": treks
    }), 200

@trekker_bp.route("/treks/<int:trek_id>/book", methods=["POST"])
@jwt_required()
@trekker_required
def book_trek(trek_id):

    user_id = int(get_jwt_identity())

    try:

        booking = TrekkerService.book_trek(
            user_id,
            trek_id
        )

        return jsonify({
            "message": "Trek booked successfully.",
            "booking": booking.to_dict()
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@trekker_bp.route("/bookings", methods=["GET"])
@jwt_required()
@trekker_required
def get_booking_history():

    user_id = int(get_jwt_identity())

    bookings = TrekkerService.get_booking_history(
        user_id
    )

    return jsonify({
        "bookings": bookings
    }), 200

@trekker_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
@trekker_required
def cancel_booking(booking_id):

    user_id = int(get_jwt_identity())

    try:

        TrekkerService.cancel_booking(
            user_id,
            booking_id
        )

        return jsonify({
            "message": "Booking cancelled successfully."
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@trekker_bp.route("/profile", methods=["GET"])
@jwt_required()
@trekker_required
def profile():

    user_id = int(get_jwt_identity())

    user = TrekkerService.get_profile(user_id)

    return jsonify({
        "user": user.to_dict()
    }), 200

@trekker_bp.route("/profile", methods=["PUT"])
@jwt_required()
@trekker_required
def update_profile():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    user_id = int(get_jwt_identity())

    try:

        user = TrekkerService.update_profile(
            user_id,
            data
        )

        return jsonify({
            "message": "Profile updated successfully.",
            "user": user.to_dict()
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@trekker_bp.route("/treks/search", methods=["GET"])
@jwt_required()
@trekker_required
def search_treks():

    filters = {
        "q": request.args.get("q"),
        "location": request.args.get("location"),
        "difficulty": request.args.get("difficulty"),
        "duration": request.args.get("duration")
    }

    treks = TrekkerService.search_treks(filters)

    return jsonify({
        "treks": treks
    }), 200

@trekker_bp.route("/bookings/export", methods=["POST"])
@jwt_required()
@trekker_required
def export_bookings():

    user_id = int(get_jwt_identity())

    # Run synchronously so the file is immediately available to download
    from app.utils.csv_export import export_booking_history as export_csv
    filename = export_csv(user_id)

    return jsonify({
        "message": "Export complete. Use the download button to get your CSV.",
        "filename": filename,
        "ready": True
    }), 200

@trekker_bp.route("/bookings/download", methods=["GET"])
@jwt_required()
@trekker_required
def download_bookings():

    user_id = int(get_jwt_identity())

    filepath = os.path.join("exports", f"bookings_{user_id}.csv")

    if not os.path.exists(filepath):
        return jsonify({
            "error": "No export file found. Please export first."
        }), 404

    return send_file(
        os.path.abspath(filepath),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"my_bookings_{user_id}.csv"
    )

'''
@trekker_bp.route("/test-reminder", methods=["POST"])
@jwt_required()
@trekker_required
def test_reminder():

    task = daily_reminder.delay()

    return jsonify({
        "message": "Reminder task started.",
        "task_id": task.id
    }), 202
'''