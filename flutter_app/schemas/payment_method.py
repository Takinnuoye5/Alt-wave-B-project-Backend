from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PaymentMethodBase(BaseModel):
    name: str
    details: str

    class Config:
        orm_mode = True

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethod(PaymentMethodBase):
    id: UUID
