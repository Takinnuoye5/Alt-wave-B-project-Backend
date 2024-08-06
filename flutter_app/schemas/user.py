import re
from datetime import datetime
from typing import Optional, Union, List


from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field



class UserBase(BaseModel):
    """Base user schema"""

    id: str
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime


class UserCreate(BaseModel):
    """Schema to create a user"""

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = Field(default_factory=lambda: None)

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            value,
        ):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character."
            )
        return value
    
    
    @field_validator("phone_number")
    @classmethod
    def phone_number_must_include_country_code(cls, value):
        """
     Validates that the phone number includes a country code.

        Args:
        value (str): The phone number to validate.

        Raises:
        ValueError: If the phone number does not include a country code.

        Returns:
           str: The validated phone number.
         """
        if value and not value.startswith('+'):
            raise ValueError(
                "Phone number must include country code. Example: +123456789"
            )
        return value
        

class UserUpdate(BaseModel):
    
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[str] = None
    
class UserData(BaseModel):
    """
    Schema for users to be returned to superadmin
    """
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_deleted: bool
    is_verified: bool
    is_super_admin: bool
    created_at: datetime
    updated_at: datetime


    model_config = ConfigDict(from_attributes=True)


class AllUsersResponse(BaseModel):
    """
    Schema for all users
    """
    message: str
    status_code: int
    status: str
    page: int
    per_page: int
    total: int
    data: Union[List[UserData], List[None]]    

class AdminCreateUser(BaseModel):
    """
    Schema for admin to create a users
    """
    email: EmailStr
    first_name: str
    last_name: str
    password: str = ''
    is_active: bool = False
    is_deleted: bool = False
    is_verified: bool = False
    is_super_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class AdminCreateUserResponse(BaseModel):
    """
    Schema response for user created by admin
    """
    message: str
    status_code: int
    status: str
    data: UserData

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EmailRequest(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema to structure token data"""

    id: Optional[str]


class DeactivateUserSchema(BaseModel):
    """Schema for deactivating a user"""

    reason: Optional[str] = None
    confirmation: bool


class ChangePasswordSchema(BaseModel):
    """Schema for changing password of a user"""

    old_password: str
    new_password: str


class ChangePwdRet(BaseModel):
    """schema for returning change password response"""

    status_code: int
    message: str


class MagicLinkRequest(BaseModel):
    """Schema for magic link creation"""

    email: EmailStr


class MagicLinkResponse(BaseModel):
    """Schema for magic link respone"""

    message: str
