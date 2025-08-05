from datetime import datetime, timedelta
from typing import Set

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from starlette import status

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
blacklisted_tokens: Set[str] = set()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        return password

def verify_password(password:str, hashed:str):
    return pwd_context.verify(password,hashed)

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token:str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# Logout functions
def blacklist_token(token: str):
    """Token'ı blacklist'e ekle"""
    try:
        # Token'ın geçerli olup olmadığını kontrol et
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload:
            # In-memory set'e ekle
            blacklisted_tokens.add(token)
            return True
        return False
    except Exception as e:
        print(f"Blacklist error: {e}")
        return False


def is_token_blacklisted(token: str) -> bool:
    """Token blacklist'te mi kontrol et"""
    return token in blacklisted_tokens


def cleanup_expired_tokens():
    """Süresi dolmuş token'ları blacklist'ten temizle"""
    expired_tokens = []
    for token in blacklisted_tokens:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Token hala geçerliyse blacklist'te kalsın
        except JWTError:
            # Token süresi dolmuşsa listeden çıkar
            expired_tokens.append(token)

    for token in expired_tokens:
        blacklisted_tokens.discard(token)

    print(f"Cleaned up {len(expired_tokens)} expired tokens from blacklist")


def verify_token(token: str):
    """Token'ı doğrula ve blacklist kontrolü yap"""
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload


def logout_user(token: str):
    """Kullanıcıyı logout et"""
    try:
        # Token'ın geçerli olup olmadığını kontrol et
        payload = decode_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Token'ı blacklist'e ekle
        if blacklist_token(token):
            return {"message": "Successfully logged out"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Logout failed"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout error: {str(e)}"
        )
