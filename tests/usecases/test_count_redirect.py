import pytest

from models import Url
from tests.conftest import db_session
from usecases import count_redirect


@pytest.mark.asyncio
async def test_count_redirect(db_session):
    # Arrange
    existing_url: Url = Url(
        short_identifier="rrerqt",
        original_url="https://original.com",
        click_count=0
    )

    db_session.add(existing_url)
    await db_session.flush()
    db_session.expunge(existing_url)

    # Act
    user_click_count = 2
    updated_url: Url = None
    for click in range(user_click_count):
        updated_url = await count_redirect(
            existing_url.short_identifier,
            db_session
        )

    # Assert
    assert updated_url.click_count == existing_url.click_count + user_click_count
