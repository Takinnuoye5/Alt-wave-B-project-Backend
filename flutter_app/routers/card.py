from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from flutter_app.database import get_db
from flutter_app.models import VirtualCard
from flutter_app.services.card import VirtualCardService
from flutter_app.services.users import user_service
from flutter_app.models import User
from flutter_app.schemas import VirtualCardCreate, VirtualCardResponse
from flutter_app.utils.success_response import success_response  # Import success_response

card_router = APIRouter(prefix="/cards", tags=["Card"])

@card_router.post("/virtual-cards", response_model=VirtualCardResponse)
def create_virtual_card(
    card_data: VirtualCardCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)  # Get the authenticated user
):
    service = VirtualCardService(db)  # Pass the `db` session to the service
    # Assign the current user's ID to the card
    card_data.user_id = current_user.id  # Correctly assign the user_id
    new_card = service.create_card(card_data)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Virtual card created successfully",
        data=new_card
    )


@card_router.get("/virtual-cards/{card_id}", response_model=VirtualCardResponse)
def get_virtual_card(
    card_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)  # Add authorization
):
    service = VirtualCardService(db)  # Pass the `db` session to the service
    card = service.get_card(card_id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Virtual card retrieved successfully",
        data=card
    )
