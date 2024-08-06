from datetime import datetime, date
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re
from flutter_app.schemas.user import UserBase


class ProfileBase(BaseModel):

    id: str
    created_at: datetime
    phone_number: str
    student_id: str
    application_number: str
    date_of_birth: date
    additional_information: str
    user: UserBase


class ProfileCreateUpdate(BaseModel):

    phone_number: Optional[str] = None
    student_id: Optional[str] = None
    application_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    additional_information: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def phone_number_validator(cls, value):
        if value and not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise ValueError("Please use a valid phone number format")
        return value

    @field_validator("phone_number")
    def phone_number_must_include_country_code(cls, v):
        """
        Validates that the phone number includes a country code.

        Args:
            v (str): The phone number to validate.

        Raises:
            ValueError: If the phone number does not include a country code.

        Returns:
            str: The validated phone number.
        """
        if v and not v.startswith("+"):
            raise ValueError(
                "Phone number must include country code. Example: +123456789"
            )
        return v
