"""品牌数据模型"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.juice import Juice


class Brand(SQLModel, table=True):
    """电子烟油品牌"""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=100)
    country: str = Field(max_length=50)
    logo_url: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    juices: list["Juice"] = Relationship(back_populates="brand")
