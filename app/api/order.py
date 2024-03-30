from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.utilities import repeat_every
from app.core.socketio import socketio_manager
from app.crud import order_crud
from app.schemas import OrderCreateRequest, OrderCreateResponse, OrderFetchAllResponse
from app.models import Order
from app.main import socketio_manager

api_router = APIRouter()


@router.get("/{order_id}", response_model=OrderFetchResponse)
async def fetch(*, order_id: int):
    order = await order_crud.fetch(order_id)
    return JSONResponse(
        content=jsonable_encoder(order),
        status_code=status.HTTP_200_OK
    )


@router.post("", response_model=OrderCreateResponse)
async def create(*, order_create: OrderCreateRequest):
    new_order: Order = Order(**order_create.dict())
    try: 
        new_order: Order = await order_crud.create(new_order)
    except:
        raise HTTPException(
            detail="Unable to create order",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return JSONResponse(
        content={"order_id": new_order.id},
        status_code=status.HTTP_201_CREATED
    )


@router.put("/{order_id}", response_model=OrderUpdateResponse)
async def update(*, order_id: int):
    updated_order = await order_crud.update(order_id)
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


@router.on_event("startup")
@repeat_every(seconds=0.1)
async def attempt_trade():
    await order_crud.attempt_trade()



@router.on_event("startup")
@repeat_every(seconds=1)
async def preview_orderbook(sio: SocketManager = Depends(socketio_manager)):
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