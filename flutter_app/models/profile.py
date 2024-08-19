from sqlalchemy import Column, String, Text, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import relationship
from flutter_app.models.base_model import BaseTableModel


class Profile(BaseTableModel):
    __tablename__ = "profiles"

    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    first_name = Column(String, nullable=True)  # Student's First Name
    last_name = Column(String, nullable=True)  # Student's Last Name
    email_address = Column(String, nullable=True)  # Student's Email Address
    student_id = Column(String, nullable=True)  # Student's ID or Application Number
    phone_number = Column(String, nullable=True)  # Student's Phone Number (Optional)
    date_of_birth = Column(Date, nullable=True)  # Student's Date of Birth
    additional_information = Column(Text, nullable=True)  # Additional Information
    institution_information = Column(String, nullable=True)  # Institution Information
    payment_information = Column(String, nullable=True)  # Payment Information
    country_paying_from = Column(String, nullable=True)  # Country You Are Paying From
    discount_code = Column(String, nullable=True)  # Discount Code
    payment_for = Column(String, nullable=True)  # Payment For
    payment_by = Column(String, nullable=True)  # Payment By (Student, Third Party)
    transaction_summary = Column(Text, nullable=True)  # Transaction Summary
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="profile")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "student_id": self.student_id,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "additional_information": self.additional_information,
            "institution_information": self.institution_information,
            "payment_information": self.payment_information,
            "country_paying_from": self.country_paying_from,
            "discount_code": self.discount_code,
            "payment_for": self.payment_for,
            "payment_by": self.payment_by,
            "transaction_summary": self.transaction_summary,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user": self.user.to_dict() if self.user else None,
        }
