from app.extensions import celery
from app.services.report_service import ReportService
from app.models import User
from app.constants.roles import UserRole
from app.utils.email import send_email

import logging

logger = logging.getLogger(__name__)

@celery.task(name="monthly_report")
def monthly_report():

    filename = ReportService.generate_monthly_report()

    logger.info("=" * 50)
    logger.info("Monthly Report Generated")
    logger.info("=" * 50)
    logger.info(f"Monthly report saved to {filename}")

    admin = User.query.filter_by(role=UserRole.ADMIN.value).first()

    if admin:
        send_email(
            admin.email,
            "Monthly Trekking Report",
            f"Hello Admin,\n\nYour monthly trekking activity report has been generated successfully.\n\nYou can access it on your server at: {filename}\nOr download it directly from the Admin Dashboard -> Reports tab.\n\nBest,\nSystem"
        )
    else:
        logger.warning("No Admin user found to email the report to.")

    return filename