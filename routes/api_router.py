from fastapi import APIRouter

from routes import shorten

api_router = APIRouter()
api_router.include_router(shorten.router)