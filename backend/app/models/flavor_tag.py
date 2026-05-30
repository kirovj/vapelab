"""口味标签数据模型"""
from sqlmodel import SQLModel, Field


class FlavorTag(SQLModel, table=True):
    """口味标签"""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)


class JuiceFlavorTag(SQLModel, table=True):
    """烟油-标签关联"""
    juice_id: int = Field(foreign_key="juice.id", primary_key=True)
    tag_id: int = Field(foreign_key="flavortag.id", primary_key=True)
