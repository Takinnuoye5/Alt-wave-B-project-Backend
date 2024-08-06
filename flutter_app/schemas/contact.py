# backend/schemas/contact.py
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    message: str

    class Config:
        orm_mode = True


class ContactCreate(ContactBase):
    pass


class ContactResponseSchema(BaseModel):
    full_name: str
    email: EmailStr
    message: str


class Contact(ContactBase):
    id: int
