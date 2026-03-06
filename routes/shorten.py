from email.policy import default
from typing import Optional

from fastapi import APIRouter, HTTPException
from urllib3.http2 import orig_HTTPSConnection

from models import Url
from models.models import URLCreate
from routes.deps import SessionDep

from usecases import find_url, create_url

router = APIRouter()


@router.post("/shorten")
async def shorten(url_create: URLCreate, db_session: SessionDep):
    url: Optional[Url] = await find_url(
        str(url_create.original_url),
        db_session
    )
    if url:
        raise HTTPException(
            status_code=404,
            detail=f"url=[{str(url_create.original_url)}] already exists"
        )

    url_info: Url = await create_url(
        url_create,
        db_session
    )
    return url_info
