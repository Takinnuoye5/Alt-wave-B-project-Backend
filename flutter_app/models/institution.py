from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    schoolName = Column(String, index=True)
    countryName = Column(String, index=True)  # Use country_name
    address = Column(String, index=True)
    paymentType = Column(String, index=True)
    contactEmail = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="institutions")
