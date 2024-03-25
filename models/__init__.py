# Possibly, move this to a db.py file
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .order import Order
from .trade import Trade

# Create the database tables based on the defined models
Base.metadata.create_all(bind=engine)