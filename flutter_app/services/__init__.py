# backend/services/__init__.py
from .users import UserService
from .institution import InstitutionService
from .contact import ContactService
from .payment import PaymentService
from .student import StudentService

# Add other service imports here


__all__ = ["UserService", "InstitutionService", "ContactService", "PaymentService", "StudentService"]
