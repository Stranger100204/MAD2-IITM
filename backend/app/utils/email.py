import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def send_email(to, subject, body):
    
    email_content = f"""
==================================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
To: {to}
Subject: {subject}
--------------------------------------------------
{body}
==================================================
"""

    # Log to console
    logger.info(email_content)
    
    # Save to a file so it can be easily shown during the viva!
    try:
        with open("mock_emails.log", "a", encoding="utf-8") as f:
            f.write(email_content + "\n")
    except Exception as e:
        logger.error(f"Failed to write to mock_emails.log: {e}")