from sqlalchemy import Column, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from flutter_app.models.associations import user_institution_association
from flutter_app.models.base_model import BaseTableModel



class Institution(BaseTableModel):
    __tablename__ = "institutions"

    school_name = Column(String, nullable=False, unique=True)
    country_name = Column(String, nullable=True, unique=True)
    address = Column(Text, nullable=True)
    payment_type = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    user_id = user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    users = relationship(
        "User", secondary=user_institution_association, back_populates="institutions"
    )
   

    def __str__(self):
        return self.school_name




