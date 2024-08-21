from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flutter_app.models.base_model import Base
from uuid_extensions import uuid7


class VirtualCard(Base):
    __tablename__ = 'virtual_cards'

    id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    user_id = Column(String, ForeignKey('users.id'))  # Use String to match User.id type
    description = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    card_style = Column(String, nullable=False)
    top_up_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    user = relationship('User', back_populates='virtual_cards')
