import uuid
from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    payment_by = Column(String, index=True)
    payment_for = Column(String, index=True)
    country_from = Column(String, index=True)
    amount = Column(Numeric(10, 2))
    payment_method = Column(String, index=True)  
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    institution_id = Column(UUID(as_uuid=True), ForeignKey('institutions.id'))

    user = relationship("User", back_populates="payments")
    institution = relationship("Institution", back_populates="payments")
