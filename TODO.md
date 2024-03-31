## Roadmap
- [X] Add redis orderbook functionality
- [X] Move crud operations for orders into orderbook
- [X] Split routes into relays/controllers and routes
- [ ] Add socketio functionality
- [ ] Set async support for sqlite
- [ ] Provide auth for endpoints
- [ ] Add alembic for maintaining migrations
- [ ] Add logging functionality
- [ ] Possibly add celery or another tool for workers
- [ ] Possibly separate out trades into a separate microservice
- [ ] Create provision for a Dead Letter Queue for failed trades
- [ ] Add unit tests especially for orderbook
- [ ] Replace models on api side with pydantic schemas (and move creation to crud)

- [ ] Replace sorted sets 'ID' with an 'UpdatedAt' approach. Since this system could be gamed!

- Sort Out:
- [ ] Socketio support - How??
- [ ] Dockerfile and docker-compose.yaml ??
- [ ] I also need to sort how the F I am gonna get them to match sequentially!


## Improved Design


- Workers: 
    - celery and flower: Celery workers can be used to attempt to perform trades from a redis stream
    - gcloud functions + gcloud cloud scheduler (for setting up polling functions)

- [redis stream](): Stream to store (bid, ask) pairs which can be processed async by celery workers
- Polling: Used to generate (bid, ask) pairs from redis sorted_sets to the redis stream
- [redis sorted sets](): Two redis sorted sets (one for ask, other for bid) used for forming the
    orderbook
- [gcloud memorystore for redis](https://cloud.google.com/memorystore/docs/cluster/memorystore-for-redis-cluster-overview): Memorystore for maintaining read replica or for having a redis cluster (if multi-location)
- postgres: Acts as transactional database for maintaining orders and trades
- [asyncpg](https://magicstack.github.io/asyncpg/current/): Lib for async queries on Postgres for updating orders etc.

- Polling System could also be done using gcloud functions + gcloud scheduler (in which case a
    simple attempt_trade microservice could be setup to poll on the memorystore redis instance)


## Issues with current implementation

- Separation into multiple microservices would be preferred.
- New proposed design could be used
- No preference is given to the time the order arrived.
- Later bid orders are often preferred. (but earlier ask orders are preferred)
