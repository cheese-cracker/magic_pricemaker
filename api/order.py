from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from core.db import get_db

router = APIRouter()

@router.get("/{order_id}")
def fetch(*, order_id, db: Session = Depends(get_db)):
    order_exists = db.query(Order).get(order_id)
    if not order_exists:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return JSONResponse(
        content=order_exists.json(),
        status_code=status.HTTP_200_OK
    )


@router.post("")
async def place(*, order_create, db: Session = Depends(get_db)):
    assert order_create.quantity > 0 and order_create.price > 0
    
    # Construct Order object
    new_order = Order(
        **order_create,
        order_alive=True
    )

    # Save to database
    try:
        order_exists = db.query(Order).get(new_order.order_id)
        if not order_exists:
            db.add(new_order)
            db.commit()
        db.refresh(new_order)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to place order.",
        )

    # Place in order book
    if new_order.side == -1:
        OrderBook.place_ask_order(new_order, db)
    elif new_order.side == 1:
        OrderBook.place_bid_order(new_order, db)

    return JSONResponse(
        content={"order_id" : new_order.order_id},
        status_code=status.HTTP_201_CREATED,
    )
    



@router.put("/{order_id}")
def modify(*, order_update, order_id, db: Session = Depends(get_db)):
    order_update.order_id = order_id
    selected_order = db.query(Order).get(order_id)
    # Attempt to remove leftover order from order book 
    # If not removable then return failed and leave half-fillfulled traded.
    
    # TODO: Clarify functionality in this

    try:
        selected_order.price = order_update.price
        selected_order.quantity = order_update.quantity
        db.add(selected_order)
        db.commit()
        db.refresh(selected_order)
        
        # TODO: Add back order in order book
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to modify order.",
        )
    return JSONResponse(
        content=selected_order.json(),
        status_code=status.HTTP_200_OK
    )


@router.delete("/{order_id}")
def cancel(*, order_id, db: Session = Depends(get_db)):
    selected_order = db.query(Order).get(order_id)
    # Attempt to remove leftover order from order book 
    # If not removable then return failed and leave half-fillfulled traded.
    
    # TODO: Clarify functionality in this
    # TODO: Alternatively, if controllers are used, perform modify and set quantity to 0
    
    try:
        selected_order.order_alive = False
        db.add(selected_order)
        db.commit()
        db.refresh(selected_order)
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel order.",
        )
    return JSONResponse(
        content=selected_order.json(),
        status_code=status.HTTP_200_OK
    )



@router.get("")
def fetch_all(*, db: Session = Depends(get_db)):
    try:
        all_orders = db.query(Order).all()
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch all orders.",
        )
    return JSONResponse(
        content=[order.json() for order in all_orders],
        status_code=status.HTTP_200_OK
    )