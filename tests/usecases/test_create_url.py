import pytest
from pydantic import HttpUrl

from models.models import URLCreate, Url
from usecases import create_url


@pytest.mark.asyncio
async def test_create_url(db_session):
    # Arrange
    original_url = "https://dummy.ru/"
    url_create: URLCreate = URLCreate(
        original_url=HttpUrl(original_url)
    )

    # Act
    created_url: Url = await create_url(
        url_create,
        db_session
    )

    # Assert
    assert created_url.original_url == original_url

    assert created_url.id is not None
    assert created_url.short_identifier is not None
    assert created_url.click_count is not None
    assert created_url.version_id is not None
    assert created_url.created_at is not None