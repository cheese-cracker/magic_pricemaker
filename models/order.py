from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from . import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    side = Column(Integer)
    order_price = Column(Numeric(precision=10, scale=2), index=True)
    order_quantity = Column(Integer)
    order_alive = Column(Boolean)
    total_traded_price = Column(Numeric(precision=10, scale=2), default=0)
    traded_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def trade(self, taking_price, taking_quantity):
        self.traded_quantity += taking_quantity
        self.total_traded_price += taking_price * taking_quantity
        if self.traded_quantity == self.order_quantity:
            self.order_alive = False
