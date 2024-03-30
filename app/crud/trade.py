from typing import List
from app.core.db import SessionLocal
from app.models.trade import Trade


class TradeCRUD():
    def __init__(self, session_maker):
        self.seismic = session_maker

    async def create(self, new_trade: Trade) -> Trade:
        async with self.seismic() as session:
            session.add(new_trade)
            await session.commit()
            await session.refresh(new_trade)
            return new_trade

    async def read(self, trade_id: int) -> Trade:
        async with self.seismic() as session:
            return session.query(Trade).get(trade_id)

    async def read_all(self) -> List[Trade]:
        async with self.seismic() as session:
            return session.query(Trade).all()
        

trade_crud = TradeCRUD(SessionLocal)