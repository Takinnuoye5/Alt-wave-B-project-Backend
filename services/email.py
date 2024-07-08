# import os
# import requests
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
# MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')

# def send_confirmation_email(to_email: str, school_name: str):
#     try:
#         response = requests.post(
#             f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
#             auth=("api", MAILGUN_API_KEY),
#             data={
#                 "from": f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>",
#                 "to": to_email,
#                 "subject": "Institution Registration Received",
#                 "html": f"""
#                     <p>Dear {school_name},</p>
#                     <p>Thank you for registering your institution. We have received your registration and will process it shortly.</p>
#                     <p>Regards,<br>Your Company</p>
#                 """
#             }
#         )
#         response.raise_for_status()  # Raise an exception if the request fails (non-2xx status code)
#         logger.info(f"Email sent to {to_email}")
#         return True
#     except requests.RequestException as e:
#         logger.error(f"Error sending email: {e}")
#         return False
