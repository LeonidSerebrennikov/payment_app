from pydantic import BaseModel
from datetime import datetime

class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AccountSimpleResponse(BaseModel):
    id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True