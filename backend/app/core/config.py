import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EV Charger Sharing API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://evuser:password123@db:5432/evcharger")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    class Config:
        case_sensitive = True

settings = Settings()
