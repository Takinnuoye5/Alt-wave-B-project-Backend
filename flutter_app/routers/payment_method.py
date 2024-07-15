# routers/payment_method.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from flutter_app import schemas, services
from flutter_app.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/payments/complete", response_model=schemas.Payment)
async def complete_payment(payment_id: int, payment_method: str, db: Session = Depends(get_db)):
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
