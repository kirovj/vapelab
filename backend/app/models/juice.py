"""烟油数据模型"""
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from app.models.flavor_tag import JuiceFlavorTag

if TYPE_CHECKING:
    from app.models.brand import Brand
    from app.models.review import Review
    from app.models.flavor_tag import FlavorTag


class JuiceStatus(str, Enum):
    """烟油状态"""
    PUBLISHED = "published"
    PENDING = "pending"
    ARCHIVED = "archived"


class Juice(SQLModel, table=True):
    """电子烟油"""
    id: int | None = Field(default=None, primary_key=True)
    brand_id: int = Field(foreign_key="brand.id")
    name: str = Field(index=True, max_length=150)
    flavor_profile: str | None = Field(default=None, max_length=50)
    nicotine_range: str | None = Field(default=None, max_length=50)
    vg_pg_ratio: str | None = Field(default=None, max_length=20)
    volume: str | None = Field(default=None, max_length=50)
    price_range: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None)
    image_urls: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    status: JuiceStatus = Field(default=JuiceStatus.PENDING)
    submitted_by: int | None = Field(default=None, foreign_key="user.id")
    avg_rating: float = Field(default=0.0)
    review_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    brand: "Brand" = Relationship(back_populates="juices")
    reviews: list["Review"] = Relationship(back_populates="juice")
    flavor_tags: list["FlavorTag"] = Relationship(back_populates="juices", link_model=JuiceFlavorTag)
