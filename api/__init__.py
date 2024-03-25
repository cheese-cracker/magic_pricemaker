from fastapi import APIRouter

from app.api.order import router as auth_router
from app.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(order_router, prefix="/order", tags=["order"])
api_router.include_router(health_router, prefix="/health", tags=["health"])
