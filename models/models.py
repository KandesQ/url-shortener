from datetime import datetime, UTC

from pydantic import computed_field, HttpUrl
from sqlalchemy import Column, DateTime, Integer
from sqlmodel import SQLModel, Field

from core.config import settings


class URLCreate(SQLModel):
    original_url: HttpUrl

class ShortIdentifierResponse(SQLModel):
    short_identifier: str
    created_at: datetime


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)
    short_identifier: str = Field(unique=True, max_length=10, nullable=False)
    original_url: str = Field(nullable=False)
    click_count: int = Field(default=0, nullable=False)

    version_id: int = Field(
        default=1,
        sa_column=Column(Integer, nullable=False, default=1)
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )


    __mapper_args__ = {
        "version_id_col": version_id.sa_column
    }
