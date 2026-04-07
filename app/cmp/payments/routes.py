from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from .schemas import PaymentResponse, WebhookRequest
from app.cmp.payments.service import get_user_payments, process_webhook
from app.cmp.users.dependecies import get_current_user_from_db
from app.cmp.users.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=List[PaymentResponse])
async def get_my_payments(
    current_user: User = Depends(get_current_user_from_db),
    db: AsyncSession = Depends(get_db)
):
    return await get_user_payments(db, current_user.id)

webhook_router = APIRouter(prefix="/webhook", tags=["Webhook"])

@webhook_router.post("/payment", status_code=status.HTTP_200_OK)
async def handle_payment_webhook(
    webhook_data: WebhookRequest,
    db: AsyncSession = Depends(get_db)
):
    return await process_webhook(db, webhook_data)