from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from typing import Optional, List
from app.cmp.accounts.models import Account

async def get_account_by_id(db: AsyncSession, account_id: int) -> Optional[Account]:
    result = await db.execute(select(Account).where(Account.id == account_id))
    return result.scalar_one_or_none()

async def get_accounts_by_user_id(db: AsyncSession, user_id: int) -> List[Account]:
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()

async def get_account_by_user_and_account_id(db: AsyncSession, user_id: int, account_id: int) -> Optional[Account]:
    result = await db.execute(
        select(Account).where(Account.user_id == user_id, Account.id == account_id)
    )
    return result.scalar_one_or_none()

async def create_account(db: AsyncSession, user_id: int, balance: float = 0.0) -> Account:
    account = Account(user_id=user_id, balance=balance)
    db.add(account)
    await db.flush()
    return account

async def update_account_balance(db: AsyncSession, account_id: int, new_balance: float) -> Optional[Account]:
    await db.execute(
        update(Account)
        .where(Account.id == account_id)
        .values(balance=new_balance, updated_at=datetime.utcnow())
    )
    await db.flush()
    return await get_account_by_id(db, account_id)

async def add_to_account_balance(db: AsyncSession, account_id: int, amount: float) -> Optional[Account]:
    account = await get_account_by_id(db, account_id)
    if account:
        new_balance = account.balance + amount
        return await update_account_balance(db, account_id, new_balance)
    return None