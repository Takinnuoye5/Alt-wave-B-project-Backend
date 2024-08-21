from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from flutter_app.models import VirtualCard
from flutter_app.schemas import VirtualCardCreate

class VirtualCardService:
    def __init__(self, db: Session):
        self.db = db

    def create_card(self, card_data: VirtualCardCreate, user_id:str):
        new_card = VirtualCard(
            description=card_data.description,
            card_type=card_data.card_type,
            card_style=card_data.card_style,
            top_up_amount=card_data.top_up_amount,
            currency=card_data.currency,
            user_id=card_data.user_id  # Ensure the user_id is passed correctly
        )
        self.db.add(new_card)
        self.db.commit()
        self.db.refresh(new_card)
        return new_card

    def get_card(self, card_id: int):
        card = self.db.query(VirtualCard).filter(VirtualCard.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return card