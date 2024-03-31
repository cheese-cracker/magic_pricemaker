from typing import List, Dict
from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.trade import Trade


class TradeCRUD():
    def __init__(self, session_maker):
        self.seismic = session_maker

    async def create(self, trade_create: Dict) -> Trade:
        new_trade = Trade(**trade_create)
        async with self.seismic() as session:
            session.add(new_trade)
            await session.commit()
            await session.refresh(new_trade)
            return new_trade

    async def read(self, trade_id: int) -> Trade:
        async with self.seismic() as session:
            return ( await session.execute(select(Trade).filter(Trade.trade_id == trade_id)) ).scalar()

    async def read_all(self) -> List[Trade]:
        async with self.seismic() as session:
            return ( await session.execute(select(Trade)) ).scalars().all()


trade_crud = TradeCRUD(SessionLocal)