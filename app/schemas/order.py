from pydantic import BaseModel, Field, conlist
from typing import Optional
from datetime import datetime

class OrderCreateRequest(BaseModel):
    order_price: float = Field(ge=0.0, multiple_of=0.01)
    order_quantity: int = Field(ge=0)
    side: int = Field(int, ge=-1, le=1, multiple_of=1)

class OrderCreateResponse(BaseModel):
    order_id: int


class OrderUpdateRequest(BaseModel):
    order_price: float = Field(ge=0.0, multiple_of=0.01)
    order_quantity: int = Field(ge=0)
    side: int = Field(int, ge=-1, le=1, multiple_of=1)

class OrderUpdateResponse(BaseModel):
    success: bool
    

class OrderDeleteRequest(BaseModel):
    order_id: int

class OrderDeleteResponse(BaseModel):
    success: bool


class OrderFetchRequest(BaseModel):
    order_id: int
    
class OrderFetchResponse(BaseModel):
    order_id: int
    side: int = Field(int, ge=-1, le=1, multiple_of=1)
    order_price: float = Field(ge=0.0, multiple_of=0.01)
    order_quantity: int = Field(ge=0)
    order_alive: bool
    total_traded_price: float
    traded_quantity: int
    
class OrderFetchAllResponse(BaseModel):
    orders: conlist(OrderFetchResponse)