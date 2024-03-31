
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, Numeric, ForeignKey
from . import Base
from datetime import datetime


class Trade(Base):
    __tablename__ = "trades"

    trade_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    executed_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), index=True)
    quantity: Mapped[int]
    bid_order_id: Mapped[int] = mapped_column(ForeignKey('orders.order_id'))
    ask_order_id: Mapped[int] = mapped_column(ForeignKey('orders.order_id'))

    def __repr__(self):
        return f"""Trade(
            trade_id={self.trade_id},
            executed_time={self.executed_time},
            price={self.price},
            quantity={self.quantity},
            bid_order_id={self.bid_order_id},
            ask_order_id={self.ask_order_id}
        )"""