from datetime import date, timedelta

from app.models import Booking, Trek
from app.constants.status import TrekStatus, BookingStatus


class ReminderService:

    @staticmethod
    def get_upcoming_users():

        tomorrow = date.today() + timedelta(days=1)

        bookings = Booking.query.join(Trek).filter(
            Booking.status == BookingStatus.BOOKED.value,
            Trek.status == TrekStatus.OPEN.value,
            Trek.start_date == tomorrow
        ).all()

        reminders = []

        for booking in bookings:

            reminders.append({
                "user": booking.user.email,
                "trek": booking.trek.name,
                "start_date": booking.trek.start_date.isoformat()
            })

        return reminders