# routers/payment.py
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from pydantic import condecimal
from decimal import Decimal
from flutter_app import schemas
from flutter_app.services.payment import PaymentService  # Correct import
from flutter_app.database import get_db
from flutter_app.middleware import get_current_user
from flutter_app.models import User
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/payments/", response_model=schemas.Payment)
async def create_payment(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    payment_by: str = Form(None),
    payment_for: str = Form(None),
    payment_method: str = Form(None),
    country_from: str = Form(None),
    amount: condecimal(max_digits=10, decimal_places=2) = Form(None)
):
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        payment = schemas.PaymentCreate(
            payment_by=payment_by,
            payment_for=payment_for,
            payment_method=payment_method,
            country_from=country_from,
            amount=Decimal(amount)
        )
    else:
        json_data = await request.json()
        payment = schemas.PaymentCreate(**json_data)
    
    try:
        logger.info(f"Received data: {payment}")
        created_payment = PaymentService.create_payment(db, payment, user_id=current_user.id, institution_id=None)
        logger.info(f"Created payment: {created_payment}")
        return created_payment
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
