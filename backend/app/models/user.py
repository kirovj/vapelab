"""用户数据模型"""
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """用户"""
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True, max_length=120)
    hashed_password: str = Field(max_length=128)
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
