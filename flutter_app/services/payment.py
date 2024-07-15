# services/payment.py
import uuid
from sqlalchemy.orm import Session
from flutter_app.models.payment import Payment
from flutter_app.schemas.payment import PaymentCreate
import logging

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
                payment_method=payment.payment_method, 
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
    def complete_payment(db: Session, payment_id: uuid.UUID, payment_method: str) -> Payment:
        try:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                raise HTTPException(status_code=404, detail="Payment not found")
            payment.payment_method = payment_method
            db.commit()
            db.refresh(payment)
            return payment
        except Exception as e:
            logger.error(f"Error completing payment: {e}")
            db.rollback()
            raise
