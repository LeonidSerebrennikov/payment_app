from pydantic import BaseModel
from datetime import datetime

class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    user_id: int
    account_id: int
    amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WebhookRequest(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float
    signature: str