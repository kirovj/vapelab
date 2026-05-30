"""评分评论数据模型"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.juice import Juice
    from app.models.user import User


class Review(SQLModel, table=True):
    """用户评分评论"""
    id: int | None = Field(default=None, primary_key=True)
    juice_id: int = Field(foreign_key="juice.id")
    user_id: int = Field(foreign_key="user.id")
    rating: int = Field(ge=1, le=10)
    comment: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    juice: "Juice" = Relationship(back_populates="reviews")
    user: "User" = Relationship()
