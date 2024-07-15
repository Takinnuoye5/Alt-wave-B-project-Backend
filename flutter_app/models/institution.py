import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    school_name = Column(String, index=True)
    country_name = Column(String, index=True)
    address = Column(String, index=True)
    payment_type = Column(String, index=True)
    contact_email = Column(String, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship("User", back_populates="institutions")
