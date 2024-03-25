
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from . import Base
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"
    trade_id = Column(Integer, primary_key=True, index=True)
    executed_time = Column(DateTime, default=datetime.utcnow)
    price = Column(Numeric(precision=10, scale=2), index=True)
    quantity = Column(Integer)
    bid_order_id = Column(Integer, ForeignKey('orders.order_id'))
    ask_order_id = Column(Integer, ForeignKey('orders.order_id'))
