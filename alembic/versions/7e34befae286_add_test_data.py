"""add test data

Revision ID: 7e34befae286
Revises: 7d5b322f62fe
Create Date: 2026-04-07 13:58:45.594262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from passlib.context import CryptContext
import os
from dotenv import load_dotenv


# revision identifiers, used by Alembic.
revision: str = '7e34befae286'
down_revision: Union[str, None] = '7d5b322f62fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def upgrade() -> None:
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_full_name = os.getenv("ADMIN_FULL_NAME", "System Administrator")

    connection = op.get_bind()

    admin_check = connection.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": admin_email}
    ).fetchone()
    
    if not admin_check:
        admin_result = connection.execute(
            sa.text("""
                INSERT INTO users (email, hashed_password, full_name, is_superuser, created_at, updated_at)
                VALUES (:email, :password, :full_name, :is_superuser, :created_at, :updated_at)
                RETURNING id
            """),
            {
                "email": admin_email,
                "password": get_password_hash(admin_password),
                "full_name": admin_full_name,
                "is_superuser": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        admin_id = admin_result.fetchone()[0]
    
    test_email = "user@example.com"
    test_password = "user123"
    test_full_name = "Test User"
    
    test_check = connection.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": test_email}
    ).fetchone()
    
    if not test_check:
        test_result = connection.execute(
            sa.text("""
                INSERT INTO users (email, hashed_password, full_name, is_superuser, created_at, updated_at)
                VALUES (:email, :password, :full_name, :is_superuser, :created_at, :updated_at)
                RETURNING id
            """),
            {
                "email": test_email,
                "password": get_password_hash(test_password),
                "full_name": test_full_name,
                "is_superuser": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        test_id = test_result.fetchone()[0]
        account_result = connection.execute(
            sa.text("""
                INSERT INTO accounts (user_id, balance, created_at, updated_at)
                VALUES (:user_id, :balance, :created_at, :updated_at)
                RETURNING id
            """),
            {
                "user_id": test_id,
                "balance": 100.0, 
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        account_id = account_result.fetchone()[0]
    else:
        account_check = connection.execute(
            sa.text("SELECT id FROM accounts WHERE user_id = :user_id"),
            {"user_id": test_id}
        ).fetchone()
        
        if not account_check:
            account_result = connection.execute(
                sa.text("""
                    INSERT INTO accounts (user_id, balance, created_at, updated_at)
                    VALUES (:user_id, :balance, :created_at, :updated_at)
                    RETURNING id
                """),
                {
                    "user_id": test_id,
                    "balance": 100.0,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            )
            account_id = account_result.fetchone()[0]

def downgrade() -> None:
    connection = op.get_bind()
    
    test_email = "user@example.com"
    
    test_user = connection.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": test_email}
    ).fetchone()
    
    if test_user:
        connection.execute(
            sa.text("DELETE FROM accounts WHERE user_id = :user_id"),
            {"user_id": test_user[0]}
        )
        connection.execute(
            sa.text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": test_user[0]}
        )
