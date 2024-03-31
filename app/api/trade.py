from fastapi import APIRouter, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any
from app.crud.trade import trade_crud
from app.schemas.trade import TradeCreateRequest, TradeCreateResponse, TradeFetchAllResponse
from app.models.trade import Trade
from app.core.socketio import sio


router = APIRouter()
@router.get("/{trade_id}")
async def fetch(trade_id: int) -> Any:
    print(trade_id)
    return {"success": True}




# , response_model=TradeFetchAllResponse
    # trade = await trade_crud.read(trade_id)
    # return JSONResponse(
    #     content=jsonable_encoder(trade),
    #     status_code=status.HTTP_200_OK
    # )


@router.post("", response_model=TradeCreateResponse)
async def create(*, trade_create: TradeCreateRequest):
    try: 
        print(trade_create)
        new_trade: Trade = await trade_crud.create(trade_create.dict())
        print(new_trade)
    except:
        # TODO: Place in DLQ in redis itself?
        raise HTTPException(
            detail="Trade creation failed! Orderbook may be out of sync!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    # await sio.emit(
    #     "trade",
    #     {
    #         "trade_id": new_trade.id,
    #         "price": new_trade.price,
    #         "quantity": new_trade.quantity,
    #         "executed_time": new_trade.executed_time,
    #         "bid_order_id": new_trade.bid_order_id,
    #         "ask_order_id": new_trade.ask_order_id
    #     }
    # )
    return JSONResponse(
        content={"trade_id": new_trade.trade_id},
        status_code=status.HTTP_201_CREATED
    )


@router.get("", response_model=TradeFetchAllResponse)
async def fetch_all():
    trades = await trade_crud.read_all()
    response = jsonable_encoder({
        "trades": [
        {
           "trade_id": trade.trade_id,
           "price": trade.price,
           "quantity": trade.quantity,
           "execution_time": trade.executed_time,
           "bid_order_id": trade.bid_order_id,
           "ask_order_id": trade.ask_order_id
        } for trade in trades
        ]
    })
    return JSONResponse(content=response)
