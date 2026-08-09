from app.extensions import db
from app.models import Trek, Booking
from app.constants.status import (
    BookingStatus,
    TrekStatus
)
from app.models import User
from app.utils.security import hash_password

class TrekkerService:

    @staticmethod
    def get_dashboard(user_id):

        booked = Booking.query.filter_by(
            user_id=user_id
        ).count()

        upcoming = Booking.query.join(
            Booking.trek
        ).filter(
            Booking.user_id == user_id,
            Booking.trek.has(status=TrekStatus.OPEN.value)
        ).count()

        completed = Booking.query.join(
            Booking.trek
        ).filter(
            Booking.user_id == user_id,
            Booking.trek.has(status=TrekStatus.COMPLETED.value)
        ).count()

        return {
            "statistics": {
                "booked_treks": booked,
                "upcoming_treks": upcoming,
                "completed_treks": completed
            }
        }

    @staticmethod
    def get_available_treks():

        treks = Trek.query.filter(
            Trek.available_slots > 0,
            Trek.status == TrekStatus.OPEN.value
        ).order_by(
            Trek.start_date.asc()
        ).all()

        return [
            trek.to_dict()
            for trek in treks
        ]

    @staticmethod
    def search_treks(filters):

        query = Trek.query.filter(
            Trek.available_slots > 0,
            Trek.status == TrekStatus.OPEN.value
        )

        if filters.get("q"):
            query = query.filter(
                Trek.name.ilike(f"%{filters['q']}%")
            )

        if filters.get("location"):
            query = query.filter(
                Trek.location.ilike(f"%{filters['location']}%")
            )

        if filters.get("difficulty"):
            query = query.filter(
                Trek.difficulty == filters["difficulty"]
            )

        if filters.get("duration"):
            query = query.filter(
                Trek.duration_days == int(filters["duration"])
            )

        treks = query.order_by(
            Trek.start_date.asc()
        ).all()

        return [
            trek.to_dict()
            for trek in treks
        ]

    @staticmethod
    def book_trek(user_id, trek_id):

        trek = Trek.query.get(trek_id)

        if not trek:
            raise ValueError("Trek not found.")

        if trek.status == TrekStatus.COMPLETED.value:
            raise ValueError("This trek has already been completed.")

        if trek.status != TrekStatus.OPEN.value:
            raise ValueError("This trek is not open for booking.")

        if trek.available_slots <= 0:
            raise ValueError("No slots available.")

        existing_booking = Booking.query.filter_by(
            user_id=user_id,
            trek_id=trek_id
        ).first()

        if existing_booking:
            raise ValueError("You have already booked this trek.")

        booking = Booking(
            user_id=user_id,
            trek_id=trek_id,
            status=BookingStatus.BOOKED.value
        )

        trek.available_slots -= 1

        db.session.add(booking)
        db.session.commit()

        return booking

    @staticmethod
    def get_booking_history(user_id):

        bookings = Booking.query.filter_by(
            user_id=user_id
        ).order_by(
            Booking.booking_date.desc()
        ).all()

        return [
            {
                **booking.to_dict(),
                "trek": booking.trek.to_dict()
            }
            for booking in bookings
        ]

    @staticmethod
    def cancel_booking(user_id, booking_id):

        booking = Booking.query.filter_by(
            id=booking_id,
            user_id=user_id
        ).first()

        if not booking:
            raise ValueError("Booking not found.")

        if booking.trek.status == TrekStatus.COMPLETED.value:
            raise ValueError("Completed trek bookings cannot be cancelled.")

        booking.trek.available_slots += 1

        db.session.delete(booking)

        db.session.commit()

    @staticmethod
    def get_profile(user_id):

        user = User.query.get(user_id)

        return user

    @staticmethod
    def update_profile(user_id, data):

        user = User.query.get(user_id)

        if not user:
            raise ValueError("User not found.")

        if data.get("name"):
            user.name = data["name"]

        if data.get("phone"):
            user.phone = data["phone"]

        if data.get("email"):
            user.email = data["email"]

        if data.get("password"):
            user.password_hash = hash_password(
                data["password"]
            )

        db.session.commit()

        return user