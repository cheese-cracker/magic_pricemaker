from typing import List, Dict, Optional
from redis import Redis
from app.models.order import Order
from app.core.redis_db import redis_db
from app.core.config import settings


class OrderBook:
    def __init__(self, *, redis_db: Redis, ask_set:str, bid_set:str):
        self.r = redis_db
        self.ask_set = ask_set
        self.bid_set = bid_set

    async def insert_ask_order(self, place_order: Order):
        return await self.r.zadd(self.ask_set, {str(place_order.order_id): place_order.order_price})
    
    async def insert_bid_order(self, place_order: Order):
        return await self.r.zadd(self.bid_set, {str(place_order.order_id): place_order.order_price})

    async def remove_ask_order(self, place_order: Order) -> int:
        return await self.r.zrem(self.ask_set, {str(place_order.order_id): place_order.order_price})
    
    async def remove_bid_order(self, place_order: Order) -> int:
        return await self.r.zrem(self.bid_set, {str(place_order.order_id): place_order.order_price})
    
    async def generate_trade_pair(self) -> tuple[Optional[int], Optional[int]]:
        """
        A function that generates a trade pair by popping values from two sets and comparing them. 
        Notes:
            - In a scalable version, this function would move data to another message queue for processing.
            - Both min and max price must be non-empty
            - No preference is given to which order goes first
            - Min price must be less than or equal to max price
            - TODO: Any error can cause OrderBook to get out of sync
        Returns:
            (min_ask_order_id, max_bid_order_id)
            (None, None)
        Raises:
            Exception: Orderbook may be out of sync.
        """
        
        try: 
            if len( min_ask_values := await self.r.zpopmin(self.ask_set) ) > 0:
                min_ask_pair = min_ask_values[0]
            else:
                return None, None

            if len( max_bid_values := await self.r.zpopmin(self.bid_set) ) > 0:
                max_bid_pair = max_bid_values[0]
            else:
                await self.r.zadd(self.ask_set, min_ask_pair)
                return None, None

            if float(min_ask_pair[1]) > float(max_bid_pair[1]):
                await self.r.zadd(self.ask_set, min_ask_pair)
                await self.r.zadd(self.bid_set, max_bid_pair)
                return None, None
        except Exception as error:
            raise Exception(
                "Failed to generate trade pair. Order book may be out of sync!",
                error
            )

        min_ask_order_id = int(min_ask_pair[0])
        max_bid_order_id = int(max_bid_pair[0])
        
        return min_ask_order_id, max_bid_order_id

    async def preview_orderbook(self) -> Dict[str, List[int]]:
        max_bid_pairs = map(int, self.r.zrevrange(self.bid_set, -5, -1))
        min_ask_pairs = map(int, self.r.zrange(self.ask_set, 0, 4))
        return {
            "bids": max_bid_pairs,
            "asks": min_ask_pairs
        }


orderbook = OrderBook(
    redis_db=redis_db,
    ask_set=settings.REDIS_ASK_SET,
    bid_set=settings.REDIS_BID_SET
)
