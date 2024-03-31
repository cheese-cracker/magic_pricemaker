# Dunno what this does but let's hope build works: https://stackoverflow.com/questions/77086128/how-to-pass-worker-options-parameters-in-gunicorn
from uvicorn.workers import UvicornWorker

class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "asyncio"}