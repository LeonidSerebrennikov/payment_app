from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import hashlib
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_webhook_signature(data: Dict[str, Any]) -> str:
    filtered_data = {k: v for k, v in data.items() if k != 'signature'}
    sorted_keys = sorted(filtered_data.keys())

    concat_string = ''.join(str(filtered_data[key]) for key in sorted_keys)
    
    concat_string += settings.WEBHOOK_SECRET_KEY
    signature = hashlib.sha256(concat_string.encode()).hexdigest()
    
    return signature

def verify_webhook_signature(data: Dict[str, Any], signature: str) -> bool:
    expected_signature = generate_webhook_signature(data)
    return signature == expected_signature
