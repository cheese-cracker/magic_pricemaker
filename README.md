## Quickstart

- Install docker-compose
- Run `docker compose up -d`.
- Visit `http://localhost:8080/docs` for the swagger UI for the API endpoints

## Design

### Current Design
![Current Implementation drawio](https://github.com/cheese-cracker/magic_pricemaker/assets/30256734/ca327997-79a8-49f8-92b8-bb2049e0b1f0)



Pros:
- Single microservice makes it easy to deploy and maintain
- Redis DB sorted sets allowing all operations involving matching orders etc. to be completed in O(logN) time. (N = no. of orders in set)
- All operations on a transaction db are write operations or are update/read operations using index. So these operations should be relatively fast.
- Order + Orderbook API and Trade API are loosely coupled so this could be split into two different microservices.
- Running FastAPI with uvicorn would allow us to spin up more instances. (Otherwise we could instead use kubernetes?)
- Most operations can be run async

Cons:
- Creation of trades could be separated out into a separate microservice
- Provision for a Dead Letter Queue for failed trades
- Unit tests especially for orderbook
- Orders are NOT executed sequentially, however if two orders have the same price the older one is selected.


### Matching Mechanisms

1. Match (max bid order, min ask order) pair:
    - Approach: 
        - Always match (max bid order, min ask order)
    - Pros:
        - Relative simple and straightforward.
        - Leverage existing scalable tools like Redis sorted sets.
    - Cons:
        - Taking away max-ask and min-bid orders could take away opportunity from other order-pairs
            from being formed. 
        - Doesn't provide first preference to oldest order
2. Order fulfilment is attempted at placement:
    - Approach: 
        - Match (max ask order,  current order) or vice versa
    - Pros:
        - Relative simple and straightforward
        - Leverages existing scalable tools like Redis sorted sets
        - Atleast one order is matched in sequence of it's arrival.
    - Cons:
        - Order matching and placement are tightly coupled
        - Still takes away opportunity from other order-pairs from being formed. 
        - Doesn't provide first preference to oldest order
3. Match closest (ask, bid) pair
    - Approach: 
        - Binary search for lower_bound/upper_bound to find the ask/bid order with price closest to the given score.
        -  Match the order.
    - Pros:
        - Allows more orders to get matched than in the matching of (min_ask order, max_bid order)
    - Cons:
        - Still doesn't provide first preference to oldest order
        - No existing tools for building this in a scalable manner. May require further deep dive.
4. Multiple Sets each with priority:
    - Approach:
        - Oldest orders go in the max priority set
        - Newer orders go in a lesser priority set and so on (similar to priority scheduling with
            aging?)
        - Sets could use any of the  previous approach to perform searches and match the order.
    - Pros:
        - Provides a preference towards older orders in orderbook
    - Cons:
        - Does not match order sequence still


One approach is we can combine 2, 3 and 4 to form a fairly optimal order book.
Where,

2. Order fulfilment can be attempted as-soon-as they arrive. Thus, atleast partially processing
   orders in-sequence of their arrival.
3. Closest orders can be matched thus provide room for more orders to be matched more easily.
4. Earlier orders are provided a preference. (due to the priority scheduler)

However, the implementation of this design with scale is still a major concern. 
The current approach is a simple version of 1.

Possible Solution with regards to this implementation:
- Using `redis.zrange` withscores, we could select a finite no. of orders within a range of prices below i.t 
- Suppose by selecting 100 orders in range (0, current_bid_price), we can match the current bid
    order to the oldest ask order in this range
- This method provides a fairly optimal approach combining some of the aspects of the 2, 3, 4 methods


## Troubleshooting

In the rare case sqlite 'testdb' and 'redis' get out of sync, it may throw errors.
If you use docker simply run `docker compose down` and then `docker compose up -d` to rerun the application afresh.


In case you run without docker compose,
Delete the 'testdb' (DATABASE_URL)
And run,
```python
from redis import Redis
from redis import Redis
r = Redis(host='localhost', port=6379)
# Delete ask and bid sets (REDIS_ASK_SET and REDIS_BID_SET) to prevent stale order_ids
r.delete("asks")
r.delete("bids")
```

#### Alternate Method of Running Application

- Run redis on port 6379
```
docker pull redis
docker run --detach -p 6379:6379 redis
```
- Setup FastAPI application (in virtualenv or using poetry)
```bash
pip install --no-cache-dir --upgrade -r /app/requirements.txt
uvicorn app.main:app --reload
```
