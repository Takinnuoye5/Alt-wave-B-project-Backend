from .institution import Institution, InstitutionCreate, InstitutionBase
from .users import User, UserCreate, UserBase, SignIn, Token
from .contact import Contact, ContactCreate
from .payment import Payment, PaymentCreate
from .payment_method import PaymentMethod, PaymentMethodCreate
from .student import Student

from pydantic import BaseModel

class YourModel(BaseModel):
    # ... your model fields ...

    def __init__(self, **data):
        print(f"Param name: {data.keys()}, Type: {type(data.keys())}")  # Inspect input data keys
        super().__init__(**data)  # Continue with the original initialization


# This ensures that Institution and User schemas are accessible from the schemas module
