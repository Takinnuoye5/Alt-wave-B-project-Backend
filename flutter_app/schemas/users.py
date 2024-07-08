from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None  # Make phone number optional

    @validator('phone_number')
    def phone_number_must_include_country_code(cls, v):
        if v and not v.startswith('+'):
            raise ValueError('Phone number must include country code. Example: +123456789')
        return v
    

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SignIn(BaseModel):
    email: str
    password: str


class Country(BaseModel):
    name: str
    flag: str
    

class UserUpdate(BaseModel):  # Add this new schema
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]

    @validator('phone_number')
    def phone_number_must_include_country_code(cls, v):
        if v and not v.startswith('+'):
            raise ValueError('Phone number must include country code. Example: +123456789')
        return v
