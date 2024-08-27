import asyncio
from flutter_app.core.dependencies.email_sender import send_email
from flutter_app.utils.setting import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_send_email():
    logger.debug(f"MAIL_USERNAME: {settings.MAIL_USERNAME}")
    logger.debug(f"MAIL_PASSWORD: {settings.MAIL_PASSWORD}")
    logger.debug(f"MAIL_SERVER: {settings.MAIL_SERVER}")
    logger.debug(f"MAIL_PORT: {settings.MAIL_PORT}")
    recipient = "akinnuoyeti@gmail.com"
    template_name = "welcome.html"  # Make sure this template exists in your templates directory
    subject = "Test Email"
    context = {"name": "Test User"}  # Provide appropriate context for your template

    await send_email(recipient, template_name, subject, context)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_send_email())
