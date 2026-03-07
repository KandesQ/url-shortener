import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from core.optimistic_lock import OptimisticLockException, optimistic_retry_async, RetryConfig
from models import Url
from repository import find_url_by_short_id

logger = logging.getLogger(__name__)

@optimistic_retry_async(RetryConfig(base_delay=0.5))
async def count_redirect(short_id: str, db_session: AsyncSession) -> Url:
    """
    Increment count click of url with given short_id
    
    :param short_id: short identifier 
    :param db_session: async database session
    :return: updated Url 
    """
    db_obj: Url = await find_url_by_short_id(short_id, db_session)

    previous_version = db_obj.version_id

    try:
        db_obj.click_count += 1

        await db_session.commit()

        logger.info(f"Click count of Url with id=[{db_obj.id}] updated: "
                    f"previous_version=[{previous_version}], current_version=[{db_obj.version_id}]")

        return db_obj
    except StaleDataError:
        await db_session.rollback()

        await db_session.refresh(db_obj)

        logger.warning(
            f"Update conflict on Url with id=[{db_obj.id}]: "
            f"expected version={previous_version}, found={db_obj.version_id}"
        )

        raise OptimisticLockException(type(db_obj).__name__, db_obj.id)
