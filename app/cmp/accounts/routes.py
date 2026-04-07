from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.cmp.accounts.schemas import AccountResponse
from app.cmp.accounts.service import get_user_accounts, get_account
from app.cmp.users.dependecies import get_current_user_from_db
from app.cmp.users.models import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/", response_model=List[AccountResponse])
async def get_my_accounts(
    current_user: User = Depends(get_current_user_from_db),
    db: AsyncSession = Depends(get_db)
):
    return await get_user_accounts(db, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account_route(
    account_id: int,
    current_user: User = Depends(get_current_user_from_db),
    db: AsyncSession = Depends(get_db)
):
    account = await get_account(db, account_id)
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return account