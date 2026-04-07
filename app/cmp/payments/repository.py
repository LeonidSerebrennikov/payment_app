from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional, List
from app.cmp.payments.models import Payment

async def get_payment_by_transaction_id(db: AsyncSession, transaction_id: str) -> Optional[Payment]:
    result = await db.execute(
        select(Payment).where(Payment.transaction_id == transaction_id)
    )
    return result.scalar_one_or_none()

async def get_payments_by_user_id(db: AsyncSession, user_id: int) -> List[Payment]:
    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == user_id)
        .order_by(desc(Payment.created_at))
    )
    return result.scalars().all()

async def get_payments_by_account_id(db: AsyncSession, account_id: int) -> List[Payment]:
    result = await db.execute(
        select(Payment).where(Payment.account_id == account_id)
    )
    return result.scalars().all()

async def create_payment(db: AsyncSession, transaction_id: str, user_id: int, account_id: int, amount: float) -> Payment:
    payment = Payment(
        transaction_id=transaction_id,
        user_id=user_id,
        account_id=account_id,
        amount=amount,
        status="completed"
    )
    db.add(payment)
    await db.flush()
    return payment