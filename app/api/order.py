from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_utilities import repeat_every
from app.core.socketio import sio
from app.crud.order import order_crud
from typing import Any
from app.schemas.order import *
from app.models.order import Order

router = APIRouter()

@router.get("/orderbook")
async def glance_orderbook() -> Any:
    orderbook_orders = await order_crud.preview_orderbook()
    print(orderbook_orders)
    return { "success": True }


@router.get("/{order_id}", response_model=OrderFetchResponse)
async def fetch(order_fetch: OrderFetchRequest):
    order = await order_crud.fetch(order_fetch.order_id)
    return JSONResponse(
        content=jsonable_encoder(order),
        status_code=status.HTTP_200_OK
    )


@router.post("", response_model=OrderCreateResponse)
async def create(*, order_create: OrderCreateRequest):
    try: 
        new_order: Order = await order_crud.create(order_create.dict())
    except Exception as error:
        print(error)
        raise HTTPException(
            detail="Unable to create order",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return JSONResponse(
        content={"order_id": new_order.id},
        status_code=status.HTTP_201_CREATED
    )


@router.put("/{order_id}", response_model=OrderUpdateResponse)
async def update(*, order_update: OrderUpdateRequest):
    updated_order = await order_crud.update(order_update.dict(exclude_unset=True))
    return JSONResponse(
        content={"success": True},
        status_code=status.HTTP_200_OK
    )


@router.delete("/{order_id}", response_model=OrderDeleteResponse)
async def delete(*, order_id: int):
    await order_crud.delete(order_id)
    return JSONResponse(
        content={"success": True},
        status_code=status.HTTP_200_OK
    )


@router.get("", response_model=OrderFetchAllResponse)
async def fetch_al():
    order_list = await order_crud.fetch_all()
    return JSONResponse(
        content={ "orders" : [jsonable_encoder(order) for order in order_list] },
        status_code=status.HTTP_200_OK
    )


@router.on_event("startup")
@repeat_every(seconds=0.1)
async def attempt_trade():
    await order_crud.attempt_trade()



@router.on_event("startup")
@repeat_every(seconds=1)
async def preview_orderbook():
    orderbook_orders = await order_crud.preview_orderbook()
    # NOTE: Only provides the last 5 bids and asks orders NOT prices
    await sio.emit(
        "orderbook",
        {
            "bids": [
                {
                    "order_id": order.order_id,
                    "price": order.price,
                    "quantity": order.quantity
                } for order in orderbook_orders["bids"]
            ],
            "asks": [
                {
                    "order_id": order.order_id,
                    "price": order.price,
                    "quantity": order.quantity
                } for order in orderbook_orders["asks"]
            ]
        }
    )