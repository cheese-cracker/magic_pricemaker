import secrets
from typing import Dict, List

from fastapi import status
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "OrdersAPI"
    DATABASE_URL = "sqlite:///./test.db"

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
