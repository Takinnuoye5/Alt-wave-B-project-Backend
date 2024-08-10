from .institution import CreateInstitution, InstitutionBase
from .user import UserCreate, UserBase, Token
from .contact import Contact, ContactCreate
from .payment import PaymentBase
from .student import Student
from .transaction import TransactionSummary

from pydantic import BaseModel


class YourModel(BaseModel):
    # ... your model fields ...

    def __init__(self, **data):
        print(
            f"Param name: {data.keys()}, Type: {type(data.keys())}"
        )  # Inspect input data keys
        super().__init__(**data)  # Continue with the original initialization


# This ensures that Institution and User schemas are accessible from the schemas module
