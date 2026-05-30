"""品牌请求/响应模型"""
from pydantic import BaseModel


class BrandCreate(BaseModel):
    """创建品牌请求"""
    name: str
    country: str
    logo_url: str | None = None
    description: str | None = None


class BrandUpdate(BaseModel):
    """更新品牌请求"""
    name: str | None = None
    country: str | None = None
    logo_url: str | None = None
    description: str | None = None


class BrandResponse(BaseModel):
    """品牌响应"""
    id: int
    name: str
    country: str
    logo_url: str | None
    description: str | None
    juice_count: int = 0
    created_at: str
