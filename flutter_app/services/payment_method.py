# services/payment_method.py
from sqlalchemy.orm import Session
from flutter_app.models.payment_method import PaymentMethod
from flutter_app.schemas.payment_method import PaymentMethodCreate
import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

class PaymentMethodService:
    @staticmethod
    def create_payment_method(db: Session, payment_method: PaymentMethodCreate, user_id: uuid.UUID) -> PaymentMethod:
        try:
            db_payment_method = PaymentMethod(
                id=uuid.uuid4(),
                name=payment_method.name,
                details=payment_method.details,
                user_id=user_id
            )
            db.add(db_payment_method)
            db.commit()
            db.refresh(db_payment_method)
            return db_payment_method
        except Exception as e:
            logger.error(f"Error creating payment method: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_payment_methods(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
        try:
            return db.query(PaymentMethod).filter(PaymentMethod.user_id == user_id).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error retrieving payment methods: {e}")
            raise

    @staticmethod
    def get_payment_method(db: Session, payment_method_id: uuid.UUID) -> Optional[PaymentMethod]:
        try:
            return db.query(PaymentMethod).filter(PaymentMethod.id == payment_method_id).first()
        except Exception as e:
            logger.error(f"Error retrieving payment method: {e}")
            raise
