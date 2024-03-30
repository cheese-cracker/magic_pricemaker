from fastapi import APIRouter

from .health import router as health_router
from .order import router as order_router
from .trade import router as trade_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(order_router, prefix="/orders", tags=["order"])
api_router.include_router(trade_router, prefix="/trades", tags=["trade"])
