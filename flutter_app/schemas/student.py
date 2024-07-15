from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID

class StudentBase(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: EmailStr
    id_number: str = Field(..., alias="idNumber")
    date_of_birth: date = Field(..., alias="dateOfBirth")
    additional_info: str = Field(..., alias="additionalInfo")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        

class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: UUID
    user_id: UUID
