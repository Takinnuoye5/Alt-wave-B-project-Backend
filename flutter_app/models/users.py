import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    otp = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="user")
    institutions = relationship("Institution", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    payment_methods = relationship("PaymentMethod", back_populates="user")

