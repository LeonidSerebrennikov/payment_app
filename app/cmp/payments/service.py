from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Dict, Any
import logging
from app.cmp.payments import repository as payment_repo
from app.cmp.users import repository as user_repo
from app.cmp.accounts import repository as account_repo
from app.cmp.payments.schemas import WebhookRequest
from app.core.utils import verify_webhook_signature

logger = logging.getLogger(__name__)

async def get_user_payments(db: AsyncSession, user_id: int):
    payments = await payment_repo.get_payments_by_user_id(db, user_id)
    return payments

async def process_webhook(db: AsyncSession, webhook_data: WebhookRequest) -> Dict[str, Any]:
    data_dict = webhook_data.dict()
    signature = data_dict.pop('signature')
    
    if not verify_webhook_signature(data_dict, signature):
        logger.error(f"Invalid signature for transaction {webhook_data.transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )

    user = await user_repo.get_user_by_id(db, webhook_data.user_id)
    if not user:
        logger.error(f"User {webhook_data.user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    existing_payment = await payment_repo.get_payment_by_transaction_id(db, webhook_data.transaction_id)
    if existing_payment:
        logger.warning(f"Duplicate transaction {webhook_data.transaction_id}")
        return {"status": "already_processed", "message": "Transaction already processed"}

    account = await account_repo.get_account_by_id(db, webhook_data.account_id)
    if not account:
        account = await account_repo.create_account(db, webhook_data.user_id, 0.0)
        logger.info(f"Created new account {account.id} for user {user.id}")

    if account.user_id != webhook_data.user_id:
        logger.error(f"Account {webhook_data.account_id} does not belong to user {webhook_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account does not belong to user"
        )
    
    payment = await payment_repo.create_payment(
        db,
        transaction_id=webhook_data.transaction_id,
        user_id=webhook_data.user_id,
        account_id=account.id,
        amount=webhook_data.amount
    )
    
    updated_account = await account_repo.add_to_account_balance(db, account.id, webhook_data.amount)
    
    await db.commit()
    
    logger.info(f"Successfully processed payment {webhook_data.transaction_id} for user {user.id}")
    
    return {
        "status": "success",
        "message": "Payment processed successfully",
        "new_balance": updated_account.balance if updated_account else 0
    }