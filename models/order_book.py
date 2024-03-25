from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from . import Base
from datetime import datetime


class OrderBook():
    def preview_orderbook(self, db):
        max_bid_orders = db.filter(Order.order_alive == True and Order.side == 1).order_by(Order.order_price.desc()).limit(5)
        min_ask_orders = db.filter(Order.order_alive == True and Order.side == -1).order_by(Order.order_price).limit(5)

    def get_best_matching_order(self, order_side, db):
        if order_side == -1:
            min_ask_order = db.filter(Order.order_alive == True and Order.side == -1).order_by(Order.order_price).first()
            return min_ask_order
        elif new_order.side == 1:
            max_bid_order = db.filter(Order.order_alive == True and Order.side == 1).order_by(Order.order_price.desc()).first()
            return max_bid_order
    
    def execute_order_trade(self, ask_order, bid_order, db):
        assert ask_order.side == -1 and bid_order.side == 1
        assert ask_order.order_price <= bid_order.order_price
        
        taking_quantity = min(
            ask_order.order_quantity - ask_order.traded_quantity, 
            bid_order.order_quantity - bid_order.traded_quantity
        )

        # trade orders at asking price
        ask_order.trade(ask_order.price, taking_quantity)
        bid_order.trade(ask_order.price, taking_quantity)
        
        return ask_order, bid_order
    
    def get_best_matching_orders(self, order_side, batch_size, db):
        pass

    def place_ask_order(self, place_order, db):
        while ( 
            place_order.order_alive == True 
            and ( exist_order := self.get_best_matching_order(order_side=1, db=db) )
            and place_order.order_price <= exist_order.order_price
        ): 
            self.execute_order_trade(ask_order=place_order, bid_order=exist_order, db=db)
        return True
    
    def place_bid_order(self, place_order, db):
        while ( 
            place_order.order_alive == True 
            and ( exist_order := self.get_best_matching_order(order_side=-1, db=db) )
            and place_order.order_price >= exist_order.order_price
        ): 
            self.execute_order_trade(ask_order=exist_order, bid_order=place_order, db=db)
        return True




async def execute_trade(*, order1, order2, db):
    if order1.side == 1:
        ask_order = order1
        bid_order = order2
    else:
        ask_order = order2
        bid_order = order1

    assert ask_order.side == -1 and bid_order.side == 1

    # Create trade object
    print("trade occurred")

    # Transact order at asking side and unalive complete orders
    Order.transact_order(ask_order, bid_order, ask_order.price)

    try:
        # db.add(executed_trade)
        db.add(ask_order)
        db.add(bid_order)
        await db.commit()
        db.refresh(ask_order)
        db.refresh(bid_order)
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute trade.",
        )
    
    # emit trade event
    # socket_manager.emit("trade", data=executed_trade.json())
    
    return ask_order, bid_order