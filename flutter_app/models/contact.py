from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flutter_app.models.base_model import BaseTableModel


class Contact(BaseTableModel):
    __tablename__ = "contacts"

    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(Text, nullable=False)
    phone_number = Column(String, nullable=True)
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    user = relationship("User", back_populates="contacts")
