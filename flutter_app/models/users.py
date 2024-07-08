from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    otp = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="user")
    institutions = relationship("Institution", back_populates="user")
    sessions = relationship("Session", back_populates="user")