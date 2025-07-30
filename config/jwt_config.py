from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from dotenv import load_dotenv

# Asegurar que se carguen las variables de entorno
load_dotenv()

class JWTConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY no está configurado en las variables de entorno")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(cls, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def verify_token(cls, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            return None