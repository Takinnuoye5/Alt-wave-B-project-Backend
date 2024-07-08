import os
from twilio.rest import Client

# Directly assign the credentials
TWILIO_SID = "AC544cd082123e6cdde190b06e3ebed71e"
TWILIO_AUTH_TOKEN = "1918487a9a801f931962a2858bed8526"
TWILIO_PHONE_NUMBER = "+14156586031"


# Function to send OTP SMS
def send_otp_sms(phone_number: str, otp: str):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

# Test the send_otp_sms function
def test_send_otp_sms():
    phone_number = "+2349070760947"  # Replace with your phone number (ensure it's in international format)
    otp = "123456"  # Sample OTP for testing
    try:
        message_sid = send_otp_sms(phone_number, otp)
        print(f"OTP sent successfully! Message SID: {message_sid}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

if __name__ == "__main__":
    test_send_otp_sms()
