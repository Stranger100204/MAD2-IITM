import logging

logger = logging.getLogger(__name__)

def send_email(to, subject, body):

    logger.info("=" * 50)
    logger.info(f"Sending email to: {to}")
    logger.info(f"Subject: {subject}")
    logger.info(body)
    logger.info("=" * 50)