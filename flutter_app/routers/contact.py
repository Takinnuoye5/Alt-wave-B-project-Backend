from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from flutter_app.db.database import get_db
from flutter_app.core.responses import SUCCESS
from flutter_app.utils.success_response import success_response
from flutter_app.services.contact_us import contact_us_service
from flutter_app.schemas.contact import ContactCreate, ContactResponseSchema
from fastapi.encoders import jsonable_encoder
from flutter_app.services.users import user_service
from flutter_app.models import User

contact_us = APIRouter(prefix="/contact", tags=["Contact-Us"])


# CREATE
@contact_us.post(
    "",
    response_model=success_response,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Contact us message created successfully"},
        422: {"description": "Validation Error"},
    },
)
async def create_contact_us(
    data: ContactCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """Add a new contact us message."""
    new_contact_us_message = contact_us_service.create(db, data)
    response_data = {
        "id": new_contact_us_message.id,
        "first_name": new_contact_us_message.first_name,
        "last_name": new_contact_us_message.last_name,
        "email": new_contact_us_message.email,
        "message": new_contact_us_message.message,
        "created_at": new_contact_us_message.created_at,
        "user_id": new_contact_us_message.user_id
    }

    response = success_response(
        message="Contact us message created successfully",
        data=response_data,
        status_code=status.HTTP_201_CREATED,
    )
    return response


@contact_us.get(
    "",
    response_model=success_response,
    status_code=200,
    responses={
        403: {"description": "Unauthorized"},
        500: {"description": "Server Error"},
    },
)
def retrieve_contact_us(
    db: Session = Depends(get_db),
    admin: User = Depends(user_service.get_current_super_admin),
):
    """
    Retrieve all contact-us submissions from database
    """

    all_submissions = contact_us_service.fetch_all(db)
    submissions_filtered = list(
        map(lambda x: ContactResponseSchema.model_validate(x), all_submissions)
    )
    if len(submissions_filtered) == 0:
        submissions_filtered = [{}]
    return success_response(
        message="Submissions retrieved successfully",
        status_code=200,
        data=jsonable_encoder(submissions_filtered),
    )
