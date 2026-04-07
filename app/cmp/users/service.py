from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Optional
from app.cmp.users import repository as user_repo
from app.cmp.users.schemas import UserCreate, UserUpdate, UserResponse, UserWithAccounts
from app.core.auth import get_password_hash, verify_password, create_access_token

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await user_repo.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return user

async def login_user(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    if await user_repo.exists_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user = await user_repo.create_user(
        db,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_superuser=False
    )
    return user

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[UserResponse]:
    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> UserResponse:
    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data.dict(exclude_unset=True)
    updated_user = await user_repo.update_user(db, user_id, **update_data)
    return updated_user

async def delete_user(db: AsyncSession, user_id: int):
    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete superuser"
        )
    
    await user_repo.delete_user(db, user_id)

async def get_all_users(db: AsyncSession) -> List[UserResponse]:
    users = await user_repo.get_all_users(db)
    return users

async def get_all_users_with_accounts(db: AsyncSession) -> List[UserWithAccounts]:
    users = await user_repo.get_all_users_with_accounts(db)
    return users