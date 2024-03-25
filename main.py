import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


# TODO: figure how to secure apis in the future
# import secure

from app.core import settings, api_router

app = FastAPI(title=settings.PROJECT_NAME)

#TODO: Setup socketio manager



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
