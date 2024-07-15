# services/payment.py
from sqlalchemy.orm import Session
from flutter_app.models.payment import Payment
from flutter_app.schemas.payment import PaymentCreate
import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

class PaymentService:
    @staticmethod
    def create_payment(db: Session, payment: PaymentCreate, user_id: uuid.UUID, institution_id: uuid.UUID) -> Payment:
        try:
            db_payment = Payment(
                id=uuid.uuid4(),
                payment_by=payment.payment_by,
                payment_for=payment.payment_for,
                country_from=payment.country_from,
                amount=payment.amount,
                user_id=user_id,
                institution_id=institution_id
            )
            db.add(db_payment)
            db.commit()
            db.refresh(db_payment)
            return db_payment
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_payments(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
        try:
            return db.query(Payment).filter(Payment.user_id == user_id).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error retrieving payments: {e}")
            raise

    @staticmethod
    def get_payment(db: Session, payment_id: uuid.UUID) -> Optional[Payment]:
        try:
            return db.query(Payment).filter(Payment.id == payment_id).first()
        except Exception as e:
            logger.error(f"Error retrieving payment: {e}")
            raise
