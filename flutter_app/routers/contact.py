from fastapi import APIRouter, Depends, HTTPException, Form, Request
import logging
from sqlalchemy.orm import Session
from pydantic import EmailStr
from flutter_app import schemas, services, models
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/contacts/", response_model=schemas.Contact)
async def create_contact(
    request: Request,
    db: Session = Depends(get_db),
    first_name: str = Form(None),
    last_name: str = Form(None),
    email: EmailStr = Form(None),
    message: str = Form(None)
):
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        contact = schemas.ContactCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message
        )
    else:
        json_data = await request.json()
        contact = schemas.ContactCreate(**json_data)

    try:
        logger.debug(f"create_contact called with: {contact}")
        created_contact = services.ContactService.create_contact(db, contact)
        logger.debug(f"Created contact: {created_contact}")
        return created_contact
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contacts = services.ContactService.get_contacts(db, current_user.id, skip=skip, limit=limit)
    return contacts

@router.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_contact = services.ContactService.get_contact(db, current_user.id, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
