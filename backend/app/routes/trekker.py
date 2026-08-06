from flask import Blueprint, jsonify
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.utils.decorators import trekker_required
from app.services.trekker_service import TrekkerService


trekker_bp = Blueprint(
    "trekker",
    __name__,
    url_prefix="/api/trekker"
)


@trekker_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@trekker_required
def dashboard():

    user_id = int(get_jwt_identity())

    return jsonify(
        TrekkerService.get_dashboard(user_id)
    ), 200

@trekker_bp.route("/treks", methods=["GET"])
@jwt_required()
@trekker_required
def get_available_treks():

    treks = TrekkerService.get_available_treks()

    return jsonify({
        "treks": treks
    }), 200

@trekker_bp.route("/treks/search", methods=["GET"])
@jwt_required()
@trekker_required
def search_treks():

    query = request.args.get("q", "").strip()

    return jsonify({
        "treks": TrekkerService.search_treks(query)
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
