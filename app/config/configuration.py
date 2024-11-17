from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


load_dotenv()

class Config(BaseSettings):
    project_title: str
    backend_port: int
    is_reload: bool
    jwt_secret_key: str
    access_token_expire_minutes: int
    database_url: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    frontend_url: str
    email_verification_token_expire_minutes: int
    refresh_token_expire_minutes: int = 30     

    class Config:
        env_path = ".env"


@lru_cache()
def get_config():
    return Config()



async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = [
        {
            "field": error["loc"][-1],
            "message": error["msg"],  # The actual error message
        }
        for error in errors
    ]
    return JSONResponse(
        status_code=400,
        content={"message": "Validation failed", "errors": custom_errors}
    )
