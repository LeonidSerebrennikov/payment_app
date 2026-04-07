from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.cmp.users.schemas import (
    LoginRequest, TokenResponse, UserResponse, 
    UserCreate, UserUpdate, UserWithAccounts
)
from app.cmp.users.service import (
    login_user, create_user, get_user_by_id, 
    update_user, delete_user, get_all_users_with_accounts
)
from app.cmp.users.dependecies import get_current_user_from_db, get_current_admin_user
from app.cmp.users.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await login_user(db, login_data.email, login_data.password)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_from_db)
):
    return current_user


admin_router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

@admin_router.get("/", response_model=List[UserWithAccounts])
async def get_all_users_route(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await get_all_users_with_accounts(db)

@admin_router.get("/{user_id}", response_model=UserResponse)
async def get_user_route(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await get_user_by_id(db, user_id)

@admin_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await create_user(db, user_data)

@admin_router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await update_user(db, user_id, user_data)

@admin_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    await delete_user(db, user_id)