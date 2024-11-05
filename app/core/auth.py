from repository.database import check_database_connection
from datetime import datetime, timedelta
import jwt
from config import get_config
import bcrypt


JWT_SECRET_KEY = get_config().jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = get_config().access_token_expire_minutes
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = get_config().email_verification_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = get_config().refresh_token_expire_minutes


async def on_startup():
    await check_database_connection()
    print("Application startup: Database connection checked.")

async def on_shutdown():
    print("Application shutdown: Cleaning up resources.")


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(user_id: int):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, int(expire.timestamp())


def create_email_verification_token(user_id: int):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, int(expire.timestamp())


def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError as e:
        print("Token has expired")
        raise e
    except jwt.InvalidTokenError as e:
        print("Token is invalid")
        raise e

def verify_token_for_password_reset(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub"), payload.get("type")
    except jwt.ExpiredSignatureError as e:
        print("Token has expired")
        raise e
    except jwt.InvalidTokenError as e:
        print("Token is invalid")
        raise e


def create_password_reset_token(user_id: int):
    to_encode = {"sub": user_id, "type": "password_reset"}
    expire = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

