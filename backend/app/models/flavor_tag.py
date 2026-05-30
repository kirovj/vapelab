"""口味标签数据模型"""
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.juice import Juice


class JuiceFlavorTag(SQLModel, table=True):
    """烟油-标签关联"""
    juice_id: int = Field(foreign_key="juice.id", primary_key=True)
    tag_id: int = Field(foreign_key="flavortag.id", primary_key=True)


class FlavorTag(SQLModel, table=True):
    """口味标签"""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)

    juices: list["Juice"] = Relationship(back_populates="flavor_tags", link_model=JuiceFlavorTag)
