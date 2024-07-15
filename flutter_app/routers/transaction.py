from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from flutter_app import schemas, services
from flutter_app.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/transactions/{transaction_id}/summary", response_model=schemas.TransactionSummary)
async def get_transaction_summary(transaction_id: int, db: Session = Depends(get_db)):
    try:
        transaction_summary = services.TransactionService.get_transaction_summary(db, transaction_id)
        logger.info(f"Retrieved transaction summary: {transaction_summary}")
        return transaction_summary
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
