from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Optional
from app.cmp.accounts import repository as account_repo
from app.cmp.accounts.schemas import AccountResponse

async def get_user_accounts(db: AsyncSession, user_id: int) -> List[AccountResponse]:
    accounts = await account_repo.get_accounts_by_user_id(db, user_id)
    return accounts

async def get_account(db: AsyncSession, account_id: int) -> Optional[AccountResponse]:
    account = await account_repo.get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account

async def create_account(db: AsyncSession, user_id: int, balance: float = 0.0) -> AccountResponse:
    account = await account_repo.create_account(db, user_id, balance)
    return account

async def get_or_create_account(db: AsyncSession, user_id: int, account_id: int) -> AccountResponse:
    account = await account_repo.get_account_by_id(db, account_id)
    if not account:
        account = await account_repo.create_account(db, user_id, 0.0)
    return account