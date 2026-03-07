from fastapi import APIRouter

from routes import shorten
from routes import redirect_to_original_url
from routes import stats

api_router = APIRouter()
api_router.include_router(shorten.router)
api_router.include_router(redirect_to_original_url.router)
api_router.include_router(stats.route, prefix="/stats")