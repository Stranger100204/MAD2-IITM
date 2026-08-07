from app.extensions import celery
from app.utils.csv_export import export_booking_history as export_csv


@celery.task(name="export_booking_history")
def export_booking_history(user_id):

    filename = export_csv(user_id)

    print(f"CSV created: {filename}")

    return filename