import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from models import Url
from routes.deps import SessionDep
from repository import find_url_by_short_id
from usecases import count_redirect

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/{short_id}", response_class=RedirectResponse, status_code=302)
async def redirect_to_original_url(
        short_id: str,
        db_session: SessionDep,
        req: Request,
):
    exists: Optional[Url] = await find_url_by_short_id(
        short_id,
        db_session
    )
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"Url with short_id=[{short_id}] not found"
        )
    # Perhaps different browsers (other than Chrome) call "purpose" header in their specific way
    purpose = req.headers.get("sec-purpose")
    if purpose:
        logger.info(
            f'Duplicate request handled: user-agent:{req.headers.get("user-agent")}, '
            f'purpose: {req.headers.get("sec-purpose")}'
        )
        return exists.original_url

    redirect_url: Url = await count_redirect(
        short_id,
        db_session
    )
    await db_session.commit()

    return redirect_url.original_url