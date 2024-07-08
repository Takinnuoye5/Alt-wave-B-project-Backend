from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
from flutter_app import models, schemas, services
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.debug(f"create_contact called with: {contact}")
    return services.ContactService.create_contact(db, contact, current_user.id)

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
