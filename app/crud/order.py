from .orderbook import OrderBook, orderbook
from app.models.order import Order
from typing import List, Dict
from fastapi import HTTPException, status
from sqlalchemy import select

# Query instead of perfroming a requests call
from app.api.trade import create as api_trade_create
from app.schemas.trade import TradeCreateRequest
from app.core.db import SessionLocal


class OrderCRUD():
    def __init__(self, session_maker, orderbook: OrderBook):
        self.orderbook = orderbook
        # async session maker
        self.seismic = session_maker

    async def fetch(self, order_id: int) -> Order:
        async with self.seismic() as session:
            return session.execute(select(Order).filter(Order.order_id == order_id)).scalar()

    async def create(self, order_create: Dict) -> Order:
        new_order = Order(
            order_price=order_create["order_price"],
            order_quantity=order_create["order_quantity"],
            side=order_create["side"],
            order_alive=True
        )
        return await self.create_or_update(new_order)

    async def create_or_update(self, new_order: Order) -> Order:
        async with self.seismic() as session:
            session.add(new_order)
            # try: 
            await session.commit()
            await session.refresh(new_order)
            if new_order.side == -1 and new_order.order_alive:
                await self.orderbook.insert_ask_order(new_order)
            elif new_order.side == 1 and new_order.order_alive:
                await self.orderbook.insert_bid_order(new_order)
            # except Exception as error:
            #     raise Exception("Failed to place order.", error)
        return new_order

    async def update(self, order_update: Dict) -> Order:
        async with self.seismic() as session:
            exist_order =  ( await session.execute(select(Order).filter(Order.order_id == order_update["order_id"])) ).scalar()
            if not exist_order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
        if exist_order.side == -1:
            await self.orderbook.remove_ask_order(exist_order)
        elif exist_order.side == 1:
            await self.orderbook.remove_bid_order(exist_order)

        if "order_price" in order_update:
            exist_order.order_price = order_update["order_price"]
        if "order_quantity" in order_update:
            exist_order.order_quantity = order_update["order_quantity"]
        if "order_alive" in order_update and not order_update["order_alive"]:
            exist_order.order_alive = False

        # Check Price and Quantity modifications
        if exist_order.order_quantity <= exist_order.traded_quantity:
            exist_order.order_quantity = exist_order.traded_quantity
            exist_order.order_alive = False

        return await self.create_or_update(exist_order)


    async def delete(self, order_id: int):
        return await self.update(
            {
                "order_id": order_id,
                "order_alive": False
            }
        )

    async def fetch_all(self) -> List[Order]:
        async with self.seismic() as session:
            result = await session.execute(select(Order))
            return result.scalars().all()

    async def preview_orderbook(self) -> Dict[str, List[Order]]:
        order_id_list = await self.orderbook.preview_orderbook()
        async with self.seismic() as session:
            try: 
                ask_orders = sorted(
                    [ 
                        ( await session.execute(select(Order).filter(Order.order_id == order_id)) ).scalar() 
                        for order_id in order_id_list['asks']
                    ],
                    key=lambda order: order.order_price
                )
                bid_orders = sorted(
                    [
                        ( await session.execute(select(Order).filter(Order.order_id == order_id)) ).scalar()
                        for order_id in order_id_list['bids']
                    ],
                    key=lambda order: order.order_price,
                    reverse=True
                )
            except AttributeError:
                # TODO: Setup a clean up that removes order ids that have been deleted from db.
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Orderbook out of Sync! Stop server and remove all None IDs from orderbook."
                )
        return {
            "bids": bid_orders,
            "asks": ask_orders
        }

    async def attempt_trade(self) -> bool:
        ask_order_id, bid_order_id = await self.orderbook.generate_trade_pair()

        if ask_order_id is None or bid_order_id is None:
            return False

        async with self.seismic() as session:
            ask_order = ( await session.execute(select(Order).filter(Order.order_id == ask_order_id)) ).scalar()
            bid_order = ( await session.execute(select(Order).filter(Order.order_id == bid_order_id)) ).scalar()
           
        taking_quantity = min(
            ask_order.order_quantity - ask_order.traded_quantity, 
            bid_order.order_quantity - bid_order.traded_quantity
        )

        # NOTE: This could be changed to updated_at, if UUIDs are used.
        if ask_order.order_id <= bid_order.order_id:
            trading_price = ask_order.order_price
        elif bid_order.order_id < ask_order.order_id:
            trading_price = bid_order.order_price

        # Trade will mark alive = False if traded_quantity is full
        await ask_order.trade(trading_price, taking_quantity)
        await bid_order.trade(trading_price, taking_quantity)

        try:
            await self.create_or_update(ask_order)
            await self.create_or_update(bid_order)
            # TODO: Request on Trade API to register trade instead?
            return await api_trade_create(
                trade_create=TradeCreateRequest(
                    price=trading_price,
                    quantity=taking_quantity,
                    bid_order_id=bid_order.order_id,
                    ask_order_id=ask_order.order_id
                )
            )
        except Exception as error:
            # TODO: DLQ for this case
            raise Exception("Failed to commit trade. Orderbook may be out of sync!", error)
    

order_crud = OrderCRUD(session_maker=SessionLocal, orderbook=orderbook)