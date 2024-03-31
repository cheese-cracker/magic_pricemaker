# Possibly, move this to a db.py file

from app.core.db import Base, async_set_db
from .order import Order
from .trade import Trade
import asyncio

# Create the database tables based on the defined models
asyncio.run(async_set_db())