from typing import Optional

from fastapi import APIRouter, HTTPException

from models import Url
from repository import find_url_by_short_id
from routes.deps import SessionDep

route = APIRouter()

@route.get("/{short_id}")
async def get_redirect_count(short_id: str, db_session: SessionDep):
    url: Optional[Url] = await find_url_by_short_id(
        short_id,
        db_session
    )
    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"Url with short_id=[{short_id}] not found"
        )

    return {
        "id": url.id,
        "click_count": url.click_count
    }


