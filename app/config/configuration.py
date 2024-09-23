from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    project_title: str
    backend_port: int
    is_reload: bool
    database_url: str
    jwt_secret_key: str
    access_token_expire_minutes: int
    database_url: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    frontend_url: str
    email_verification_token_expire_minutes: int
    refresh_token_expire_days: int = 30     

    class Config:
        env_path = ".env"


@lru_cache()
def get_config():
    return Config()
