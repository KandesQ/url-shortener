import logging

from fastapi import FastAPI

from routes.api_router import api_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")