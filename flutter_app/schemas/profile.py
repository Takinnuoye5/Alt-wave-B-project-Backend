from datetime import datetime, date
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re
from flutter_app.schemas.user import UserBase


class ProfileBase(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    student_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    additional_information: Optional[str] = None
    institution_information: Optional[str] = None
    payment_information: Optional[str] = None
    country_paying_from: Optional[str] = None
    discount_code: Optional[str] = None
    payment_for: Optional[str] = None
    payment_by: Optional[str] = None
    transaction_summary: Optional[str] = None
    created_at: datetime
    user: UserBase


class ProfileCreateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    student_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    additional_information: Optional[str] = None
    institution_information: Optional[str] = None
    payment_information: Optional[str] = None
    country_paying_from: Optional[str] = None
    discount_code: Optional[str] = None
    payment_for: Optional[str] = None
    payment_by: Optional[str] = None
    transaction_summary: Optional[str] = None

    @field_validator("email_address")
    @classmethod
    def email_validator(cls, value):
        if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Please provide a valid email address")
        return value

    @field_validator("phone_number")
    @classmethod
    def phone_number_validator(cls, value):
        if value and not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise ValueError("Please use a valid phone number format")
        return value

    
