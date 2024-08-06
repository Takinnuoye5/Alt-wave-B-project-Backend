from pydantic import BaseModel, EmailStr
from typing import Optional


class OTPRequest(BaseModel):
    email: EmailStr
    otp: str


class SendOTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class GoogleOAuthCallback(BaseModel):
    id_token: str


class SignIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
