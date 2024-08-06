from sqlalchemy import Column, String, Text
from flutter_app.models.base_model import BaseTableModel


class FAQ(BaseTableModel):
    __tablename__ = "faqs"

    question = Column(String, nullable=True)
    answer = Column(Text, nullable=True)
