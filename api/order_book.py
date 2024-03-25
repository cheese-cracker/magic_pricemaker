# from fastapi import FastAPI
# from fastapi_socketio import SocketManager

# app = FastAPI()
# socket_manager = SocketManager(app)


@socket_manager.on("order_book_status")
async def emit_order_book_status(sid):
    await socket_manager.emit("order_book_status_response", data={})
