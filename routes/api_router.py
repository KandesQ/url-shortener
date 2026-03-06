from fastapi import APIRouter

from routes import shorten
from routes import redirect_to_original_url

api_router = APIRouter()
api_router.include_router(shorten.router)
api_router.include_router(redirect_to_original_url.router)