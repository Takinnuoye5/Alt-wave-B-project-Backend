# services/transaction.py
from sqlalchemy.orm import Session
from flutter_app.models import Payment, Student, Institution
import logging

logger = logging.getLogger(__name__)


class TransactionService:
    @staticmethod
    def get_transaction_summary(db: Session, transaction_id: int):
        try:
            payment = db.query(Payment).filter(Payment.id == transaction_id).first()
            student = db.query(Student).filter(Student.id == payment.student_id).first()
            institution = db.query(Institution).filter(Institution.id == payment.institution_id).first()
            
            transaction_summary = {
                "institution": {
                    "name": institution.school_name,
                    "address": institution.address,
                    "country": institution.country_name
                },
                "payment": {
                    "amount": payment.amount,
                    "payment_by": payment.payment_by,
                    "payment_for": payment.payment_for,
                    "country_from": payment.country_from,
                    "transaction_fee": payment.transaction_fee,
                    "current_rate": payment.current_rate
                },
                "student": {
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "email": student.email,
                    "id_number": student.id_number,
                    "date_of_birth": student.date_of_birth,
                    "additional_info": student.additional_info
                }
            }
            logger.info(f"Transaction summary: {transaction_summary}")
            return transaction_summary
        except Exception as e:
            logger.error(f"Error retrieving transaction summary: {e}")
            raise
