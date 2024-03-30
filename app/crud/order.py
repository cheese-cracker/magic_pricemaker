from orderbook import OrderBook, orderbook
from app.models.order import Order

# Query instead of perfroming a requests call
from app.api.trade import create as trade_create
from app.schemas.trade import TradeCreateRequest
from app.core.db import SessionLocal


class OrderCRUD():
    def __init__(self, session_maker, orderbook: OrderBook):
        self.orderbook = orderbook
        self.siesmic = session_maker

    async def create(self, new_order: Order) -> Order:
        with self.siesmic() as session:
            old_order = session.query(Order).get(new_order.order_id)
            if old_order:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Order already exists"
                )
            return await self.create_or_update(new_order)


    async def create_or_update(self, new_order: Order) -> Order:
        with self.siesmic() as session:
            session.add(new_order)
            try: 
                await session.commit()
                await session.refresh(new_order)
                if new_order.side == -1 and new_order.order_alive:
                    await self.orderbook.place_ask_order(new_order)
                elif new_order.side == 1 and new_order.order_alive:
                    await self.orderbook.place_bid_order(new_order)
            except Exception as error:
                raise Exception("Failed to place order.", error)

        return new_order

    async def update(self, new_order: Order) -> Order:
        old_order = self.db.query(Order).get(new_order.order_id)
        if old_order.side == -1:
            await self.orderbook.remove_ask_order(old_order)
        elif old_order.side == 1:
            await self.orderbook.remove_bid_order(old_order)
            
        # Check Price and Quantity modifications
        if new_order.quantity <= old_order.traded_quantity:
            new_order.order_alive = False
        
        assert new_order.traded_quantity == old_order.traded_quantity
        assert new_order.total_traded_price == old_order.total_traded_price
        
        return await self.create(new_order)
    

    async def preview_orderbook(self) -> Dict[str, List[Order]]:
        order_id_list = await self.orderbook.preview_orderbook()
        with self.siesmic() as session:
            ask_orders = sorted( 
                [ await session.query(Order).get(order_id) for order_id in order_id_list['asks'] ],
                key=lambda order: order.order_price
            )
            bid_orders = sorted( 
                [ await session.query(Order).get(order_id) for order_id in order_id_list['bids'] ],
                key=lambda order: order.order_price,
                reverse=True
            )
        return {
            "bids": bid_orders,
            "asks": ask_orders
        }
        
    async def attempt_trade(self) -> bool:
        ask_order_id, bid_order_id = self.orderbook.generate_trade_pair()

        if ask_order_id is None or bid_order_id is None:
            return False

        with self.siesmic() as session:
            ask_order = await session.query(Order).get(ask_order_id)
            bid_order = await session.query(Order).get(bid_order_id)
            
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
        ask_order.trade(trading_price, taking_quantity)
        bid_order.trade(trading_price, taking_quantity)
        
        try:
            self.create_or_update(ask_order)
            self.create_or_update(bid_order)
            # TODO: Request on Trade API to register trade instead?
            trade_create(
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
        
        return True
    

order_crud = OrderCRUD(session_maker=SessionLocal, orderbook=orderbook)
