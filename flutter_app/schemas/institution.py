from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, EmailStr, field_validator, Field
from flutter_app.utils.success_response import success_response


class InstitutionBase(BaseModel):
    """Base organization schema"""

    id: str
    school_name: str = Field(..., alias="schoolName")
    country_name: str = Field(..., alias="countryName")
    address: str
    payment_type: str = Field(..., alias="paymentType")
    contact_email: EmailStr = Field(..., alias="contactEmail")


class CreateInstitution(BaseModel):
    """Schema to create Institution"""

    school_name: str = Field(..., alias="schoolName")
    country_name: str = Field(..., alias="countryName")
    address: str
    payment_type: str = Field(..., alias="paymentType")
    contact_email: EmailStr = Field(..., alias="contactEmail")

    class Config:
        orm_mode = True
        allow_population_by_field_name = (
            True  # This allows using the alias names when creating models
        )


class PaginatedInstUsers(BaseModel):
    """Describe response object for paginated users in organization"""

    page: int
    per_page: int
    per_page: int
    total: int
    status_code: int
    success: bool
    message: str
    data: List[Dict]
