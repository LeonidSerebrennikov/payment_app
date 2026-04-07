from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.cmp.users.routes import router as auth_router, admin_router
from app.cmp.accounts.routes import router as accounts_router
from app.cmp.payments.routes import router as payments_router, webhook_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

load_dotenv()

app = FastAPI(
    title=os.getenv("PROJECT_NAME"),
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(accounts_router)
app.include_router(payments_router)
app.include_router(webhook_router)
