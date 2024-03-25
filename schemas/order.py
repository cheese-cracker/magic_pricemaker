from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    order_id: int
    # Ensure quantity is greater than 0 
    price: float = Field(ge=0.0, multiple_of=0.01)
    quantity: int = Field(ge=0)
    side: int
    timestamp: Optional[datetime]
    order_alive: int
