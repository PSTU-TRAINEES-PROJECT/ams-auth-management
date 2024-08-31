from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from pydantic import EmailStr
from config import get_config


JWT_SECRET_KEY = get_config().jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = get_config().access_token_expire_minutes
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = get_config().email_verification_token_expire_minutes

def create_access_token(email: str):
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, int(expire.timestamp())

def create_email_verification_token(email: str):
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> EmailStr:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")