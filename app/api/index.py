
from typing import Any, List
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index() -> Any:
    return {"detail": "Please visit /docs for testing api endpoints using swagger!"}