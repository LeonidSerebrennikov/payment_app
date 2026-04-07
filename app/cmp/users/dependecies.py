from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.auth import get_current_user, get_current_admin
from app.cmp.users.models import User

async def get_current_user_from_db(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_admin)
) -> User:
    return current_user