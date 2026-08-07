import csv
import os

from app.models import Booking


def export_booking_history(user_id):

    os.makedirs("exports", exist_ok=True)

    filename = f"exports/bookings_{user_id}.csv"

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Booking ID",
            "Trek",
            "Location",
            "Status",
            "Booking Date"
        ])

        for booking in bookings:

            writer.writerow([
                booking.id,
                booking.trek.name,
                booking.trek.location,
                booking.status,
                booking.booking_date.strftime("%Y-%m-%d")
                if booking.booking_date
                else ""
            ])

    return filename