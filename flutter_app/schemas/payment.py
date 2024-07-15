# schemas/payment.py
from pydantic import BaseModel, Field, condecimal
from typing import Optional
from decimal import Decimal
from uuid import UUID

class PaymentBase(BaseModel):
    payment_by: str = Field(..., alias="paymentBy")
    payment_for: str = Field(..., alias="paymentFor")
    country_from: str = Field(..., alias="countryFrom")
    amount: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: UUID
