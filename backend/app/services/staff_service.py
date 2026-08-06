from app.extensions import db
from app.models import Trek, Booking
from app.constants.status import TrekStatus

class StaffService:

    @staticmethod
    def get_dashboard(user_id):

        assigned_treks = Trek.query.filter_by(
            assigned_staff_id=user_id
        ).count()

        active_treks = Trek.query.filter_by(
            assigned_staff_id=user_id,
            status=TrekStatus.ONGOING.value
        ).count()

        completed_treks = Trek.query.filter_by(
            assigned_staff_id=user_id,
            status=TrekStatus.COMPLETED.value
        ).count()

        return {
            "statistics": {
                "assigned_treks": assigned_treks,
                "active_treks": active_treks,
                "completed_treks": completed_treks
            }
        }

    @staticmethod
    def get_assigned_treks(user_id):

        treks = Trek.query.filter_by(
            assigned_staff_id=user_id
        ).order_by(
            Trek.start_date.asc()
        ).all()

        return [
            trek.to_dict()
            for trek in treks
        ]

    @staticmethod
    def get_trek_details(user_id, trek_id):

        trek = Trek.query.filter_by(
            id=trek_id,
            assigned_staff_id=user_id
        ).first()

        if not trek:
            raise ValueError(
                "Trek not found or not assigned to you."
            )

        return trek

    @staticmethod
    def get_participants(user_id, trek_id):

        trek = Trek.query.filter_by(
            id=trek_id,
            assigned_staff_id=user_id
        ).first()

        if not trek:
            raise ValueError(
                "Trek not found or not assigned to you."
            )

        participants = []

        for booking in trek.bookings:

            participants.append({
                "booking_id": booking.id,
                "booking_date": booking.booking_date.isoformat(),
                "status": booking.status,
                "payment_status": booking.payment_status,
                "user": booking.user.to_dict()
            })

        return participants

    @staticmethod
    def update_trek_status(user_id, trek_id, status):

        trek = Trek.query.filter_by(
            id=trek_id,
            assigned_staff_id=user_id
        ).first()

        if not trek:
            raise ValueError(
                "Trek not found or not assigned to you."
            )

        trek.status = status

        db.session.commit()

        return trek

    @staticmethod
    def complete_trek(user_id, trek_id):

        trek = Trek.query.filter_by(
            id=trek_id,
            assigned_staff_id=user_id
        ).first()

        if not trek:
            raise ValueError(
                "Trek not found or not assigned to you."
            )

        trek.status = TrekStatus.COMPLETED.value

        db.session.commit()

        return trek