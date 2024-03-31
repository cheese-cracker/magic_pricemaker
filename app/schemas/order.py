from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class OrderCreateRequest(BaseModel):
    order_price: float = Field(ge=0.0, multiple_of=0.01)
    order_quantity: int = Field(ge=0)
    side: int

    @validator('side')
    def check_valid_values(cls, v):
        valid_values = [1, -1]  
        if v not in valid_values:
            raise ValueError(f'Side must be one of {valid_values}')
        return v

class OrderCreateResponse(BaseModel):
    order_id: int


class OrderUpdateRequest(BaseModel):
    order_price: Optional[float] = Field(ge=0.0, multiple_of=0.01, default=None)
    order_quantity: Optional[int] = Field(ge=0, default=None)

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
    orders: List[OrderFetchResponse]