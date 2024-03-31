from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.redis_db import redis_db

router = APIRouter()

@router.get("")
async def get_health_status() -> Any:
    return {"success": True}

@router.get("/redis")
async def redis_check():
    try:
        redis_db.ping()
        return {"success": True}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis is not available")
