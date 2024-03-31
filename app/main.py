import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import nest_asyncio


# TODO: figure how to secure apis in the future
# TODO: setup JWT auth for APIs
# import secure
from app.core.config import settings

# Declare app before importing anything else
app = FastAPI(title=settings.PROJECT_NAME)

nest_asyncio.apply()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.socketio import socket_app
from app.api import api_router

app.add_websocket_route("/", socket_app)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
