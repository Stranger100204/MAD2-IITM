from app.extensions import celery
from app.utils.csv_export import export_booking_history as export_csv
import logging

logger = logging.getLogger(__name__)

@celery.task(name="export_booking_history")
def export_booking_history(user_id):

    filename = export_csv(user_id)

    logger.info(f"CSV created: {filename}")

    return filename