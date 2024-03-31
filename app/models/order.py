from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Numeric, Boolean
from . import Base
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(nullable=False, unique=True, primary_key=True, index=True, autoincrement=True)
    order_price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    order_quantity: Mapped[int] = mapped_column(nullable=False)
    side: Mapped[int] = mapped_column(nullable=False)
    order_alive: Mapped[bool] = mapped_column(nullable=False)
    total_traded_price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), default=0)
    traded_quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    async def trade(self, taking_price, taking_quantity):
        self.traded_quantity += taking_quantity
        self.total_traded_price += taking_price * taking_quantity
        if self.traded_quantity == self.order_quantity:
            self.order_alive = False
    
    def __repr__(self):
        return f"""Order(
            order_id={self.order_id},
            side={self.side},
            order_price={self.order_price},
            order_quantity={self.order_quantity},
            order_alive={self.order_alive},
            total_traded_price={self.total_traded_price},
            traded_quantity={self.traded_quantity},
            created_at={self.created_at},
            updated_at={self.updated_at}
        )"""