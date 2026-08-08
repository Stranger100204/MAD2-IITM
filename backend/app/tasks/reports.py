from app.extensions import celery
from app.services.report_service import ReportService

import logging

logger = logging.getLogger(__name__)

@celery.task(name="monthly_report")
def monthly_report():

    filename = ReportService.generate_monthly_report()

    logger.info("=" * 50)
    logger.info("Monthly Report Generated")
    logger.info("=" * 50)
    logger.info(f"Monthly report saved to {filename}")

    return filename