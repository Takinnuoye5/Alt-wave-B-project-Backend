from pydantic import BaseModel, Field, condecimal
from typing import List, Optional
from decimal import Decimal
from uuid import UUID


class InstitutionDetails(BaseModel):
    name: str
    address: str
    country: str


class PaymentDetails(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    payment_by: str
    payment_for: str
    country_from: str
    transaction_fee: condecimal(max_digits=10, decimal_places=2)
    current_rate: condecimal(max_digits=20, decimal_places=10)


class StudentDetails(BaseModel):
    first_name: str
    last_name: str
    email: str
    id_number: str
    date_of_birth: str
    additional_info: Optional[str] = None


class TransactionSummary(BaseModel):
    institution: InstitutionDetails
    payment: PaymentDetails
    student: StudentDetails

    class Config:
        orm_mode = True
