from pydantic import BaseSettings

from core.config import settings


class APIRoutes(BaseSettings):
    pass


api_routes = APIRoutes()
