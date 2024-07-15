# routers/payment_method.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from flutter_app import schemas, services
from uuid import UUID
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user
from flutter_app.models import User
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/payments/complete", response_model=schemas.Payment)
async def complete_payment(
    payment_id: UUID,
    payment_method: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        completed_payment = services.PaymentService.complete_payment(db, payment_id, payment_method)
        logger.info(f"Completed payment: {completed_payment}")
        return completed_payment
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
