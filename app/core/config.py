import os
from typing import List
from fastapi import status
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "OrdersAPI"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    # Redis Config
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_ASK_SET: str = "asks"
    REDIS_BID_SET: str = "bids"

    SUCCESS_STATUS_CODES: List[int] = [
        status.HTTP_200_OK,
        status.HTTP_201_CREATED,
        status.HTTP_202_ACCEPTED,
    ]

    CLIENT_ERROR_STATUS_CODES: List[int] = [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_402_PAYMENT_REQUIRED,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_408_REQUEST_TIMEOUT,
        status.HTTP_409_CONFLICT,
        status.HTTP_429_TOO_MANY_REQUESTS,
    ]


settings = Settings()
