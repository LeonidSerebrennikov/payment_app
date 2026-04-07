from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Payment App")
    
    ASYNC_DATABASE_URL: str = os.getenv("ASYNC_DATABASE_URL", "")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL", "")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_FULL_NAME: str = os.getenv("ADMIN_FULL_NAME", "System Administrator")
    
    WEBHOOK_SECRET_KEY: str = os.getenv("WEBHOOK_SECRET_KEY", "gfdmhghif38yrf9ew0jkf32")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()