import random
import smtplib
from twilio.rest import Client
from email.mime.text import MIMEText
import os

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = os.getenv("MAIL_TLS").lower() in ("true", "1", "t")
MAIL_SSL = os.getenv("MAIL_SSL").lower() in ("true", "1", "t")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def send_otp_email(email: str, otp: str):
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Your OTP Code"
    msg["From"] = MAIL_FROM
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_TLS:
                server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, [email], msg.as_string())
        print("OTP email sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")


def send_otp_sms(phone_number: str, otp: str):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}", from_=TWILIO_PHONE_NUMBER, to=phone_number
    )
    return message.sid
