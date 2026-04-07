from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from typing import Optional, List
from app.cmp.users.models import User
from app.core.auth import get_password_hash

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_all_users_with_accounts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(
        select(User)
        .options(selectinload(User.accounts))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, email: str, hashed_password: str, full_name: str, is_superuser: bool = False) -> User:
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_superuser=is_superuser
    )
    db.add(user)
    await db.flush()
    return user

async def update_user(db: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
    if 'password' in kwargs:
        kwargs['hashed_password'] = get_password_hash(kwargs.pop('password'))
    
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(**kwargs)
    )
    await db.flush()
    return await get_user_by_id(db, user_id)

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(
        delete(User).where(User.id == user_id)
    )
    await db.flush()
    return result.rowcount > 0

async def exists_user_by_email(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None