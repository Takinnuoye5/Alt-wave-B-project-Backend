from pydantic import BaseModel
from typing import Optional


class VirtualCardCreate(BaseModel):
    description: str
    card_type: str  # 'single-use' or 'multi-use'
    card_style: str  # Preferred card style
    top_up_amount: int  # Initial top-up amount
    currency: str  # Currency type, e.g., 'USD'
    user_id: Optional[str] = None  # Add this line if it doesn't exist
    

class VirtualCardResponse(BaseModel):
    id: str
    description: str
    card_type: str
    card_style: str
    top_up_amount: int
    currency: str
    user_id: Optional[str] = None  # Add this to the response

    class Config:
        orm_mode = True
