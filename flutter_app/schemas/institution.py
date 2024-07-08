from pydantic import BaseModel, Field, EmailStr

class InstitutionBase(BaseModel):
    school_name: str = Field(..., alias="schoolName")
    country_name: str = Field(..., alias="countryName")
    address: str
    payment_type: str = Field(..., alias="paymentType")
    contact_email: EmailStr = Field(..., alias="contactEmail")

    def __init__(self, **data):
        print("InstitutionBase data:", data)  # Debugging statement
        super().__init__(**data)

class InstitutionCreate(InstitutionBase):
    pass

class Institution(InstitutionBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # This allows using the alias names when creating models
