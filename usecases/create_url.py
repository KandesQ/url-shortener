from sqlalchemy.ext.asyncio import AsyncSession

from models import Url
from models.models import URLCreate

import string


async def create_url(url_create: URLCreate, db_session: AsyncSession) -> Url:
    """
    Creates a Url entity from the original string url

    As a unique identifier for short url using the incremental ID approach

    :param url_create: request object
    :param db_session: async database session

    :return: created Url model
    """
    db_obj = Url.model_validate(
        url_create,
        update={
            "original_url": str(url_create.original_url),
            "short_identifier": ""
        }
    )

    db_session.add(db_obj)
    await db_session.flush()

    db_obj.short_identifier = _get_short_identifier(db_obj.id)

    await db_session.commit()
    await db_session.refresh(db_obj)

    return db_obj


_SHORT_IDENTIFIER_LENGTH = 6
_ALL_CASES_ASCII_ALPHABET = string.ascii_letters
_BASE = len(_ALL_CASES_ASCII_ALPHABET)
def _get_short_identifier(num: int) -> str:
    """
    Creates a 6 digit short identifier from given number

    The output identifier contains letters from both upper and lower cases of ASCII

    :param num: number to encode
    :return: short identifier
    """
    tmp = []
    while num > 0:
        num, remainder = divmod(num, _BASE)
        tmp.append(_ALL_CASES_ASCII_ALPHABET[remainder])

    while len(tmp) < _SHORT_IDENTIFIER_LENGTH:
        tmp.append(_ALL_CASES_ASCII_ALPHABET[0])

    return "".join(reversed(tmp))

