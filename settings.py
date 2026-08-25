from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = getenv("DATABASE_URL", "postgresql+asyncpg://admin:password@postgres_db:5432/db")
    KAFKA_BROKER_URL: str = getenv("KAFKA_BROKER_URL", "localhost:9092")

    YOOKASSA_SHOP_ID: str = getenv("YOOKASSA_SHOP_ID", "your_shop_id")
    YOOKASSA_SECRET_KEY: str = getenv("YOOKASSA_SECRET_KEY", "your_secret_key")
    YOOKASSA_RETURN_URL: str = getenv("YOOKASSA_RETURN_URL", "your_return_url")

    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY", "default_secret_key")
    ALGORITHM: str = getenv("ALGORITHM", "HS256")

    class Config:
        env_file = ".env"

settings = Settings()