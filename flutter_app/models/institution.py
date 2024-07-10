from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, index=True)
    country_name = Column(String, index=True)
    address = Column(String, index=True)
    payment_type = Column(String, index=True)
    contact_email = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="institutions")
