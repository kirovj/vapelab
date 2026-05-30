"""烟油请求/响应模型"""
from pydantic import BaseModel


class JuiceCreate(BaseModel):
    """创建烟油请求"""
    brand_id: int
    name: str
    flavor_profile: str | None = None
    nicotine_range: str | None = None
    vg_pg_ratio: str | None = None
    volume: str | None = None
    price_range: str | None = None
    description: str | None = None
    image_urls: list[str] = []
    tag_ids: list[int] = []


class JuiceUpdate(BaseModel):
    """更新烟油请求"""
    brand_id: int | None = None
    name: str | None = None
    flavor_profile: str | None = None
    nicotine_range: str | None = None
    vg_pg_ratio: str | None = None
    volume: str | None = None
    price_range: str | None = None
    description: str | None = None
    image_urls: list[str] | None = None
    tag_ids: list[int] | None = None
