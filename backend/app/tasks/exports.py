from app.extensions import celery


@celery.task(name="export_booking_history")
def export_booking_history(user_id):

    print(f"Exporting bookings for {user_id}")

    return "Done"