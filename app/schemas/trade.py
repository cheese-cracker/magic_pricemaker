from pydantic import BaseModel, Field, conlist
from typing import Optional, List
from datetime import datetime

class TradeCreateRequest(BaseModel):
    price: float = Field(ge=0.0, multiple_of=0.01)
    quantity: int = Field(ge=0)
    bid_order_id: int
    ask_order_id: int

class TradeCreateResponse(BaseModel):
    trade_id: int

class TradeFetchResponse(BaseModel):
    trade_id: int
    executed_time: datetime
    price: float
    quantity: int
    bid_order_id: int
    ask_order_id: int
    
class TradeFetchAllResponse(BaseModel):
    trades: List[TradeFetchResponse]
