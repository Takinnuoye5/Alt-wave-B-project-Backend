from mailjet_rest import Client
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")


def send_email(to_email, subject, plain_text_content, html_content):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version="v3.1")
    data = {
        "Messages": [
            {
                "From": {"Email": MAILJET_SENDER_EMAIL, "Name": "Your Name"},
                "To": [{"Email": to_email, "Name": "Recipient Name"}],
                "Subject": subject,
                "TextPart": plain_text_content,
                "HTMLPart": html_content,
            }
        ]
    }
    try:
        result = mailjet.send.create(data=data)
        logger.info(f"Email sent successfully: {result.status_code}")
        return result
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise
