from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("")
async def get_health_status() -> Any:
    return {"success": True}
