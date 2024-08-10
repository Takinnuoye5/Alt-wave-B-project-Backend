# app/models/billing_plan.py
from sqlalchemy import Column, String, ARRAY, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from flutter_app.models.base_model import BaseTableModel


class BillingPlan(BaseTableModel):
    __tablename__ = "billing_plans"

    institution_id = Column(
        String, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    description = Column(String, nullable=True)
    features = Column(ARRAY(String), nullable=False)

    institution = relationship("Institution", back_populates="billing_plans")
