import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flutter_app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    id_number = Column(String, index=True)
    date_of_birth = Column(Date)
    additional_info = Column(String, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship("User", back_populates="students")
