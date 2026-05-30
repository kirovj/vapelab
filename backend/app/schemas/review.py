"""评分评论请求/响应模型"""
from pydantic import BaseModel


class ReviewCreate(BaseModel):
    """创建评论请求"""
    juice_id: int
    rating: int
    comment: str | None = None


class ReviewUpdate(BaseModel):
    """更新评论请求"""
    rating: int | None = None
    comment: str | None = None
