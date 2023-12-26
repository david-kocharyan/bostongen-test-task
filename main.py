import logging
import uvicorn

from fastapi import FastAPI
from app.routes import router as api_router

from config import APP_HOST, APP_PORT, APP_ENV, AppEnv

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app = FastAPI()

app.include_router(
    api_router,
    tags=["App"]
)

if __name__ == "__main__":
    auto_reload = True if APP_ENV == AppEnv.DEV.value else False
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=auto_reload)
