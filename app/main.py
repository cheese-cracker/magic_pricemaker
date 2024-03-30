import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


# TODO: figure how to secure apis in the future
# TODO: setup JWT auth for APIs
# import secure

from api import api_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

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
