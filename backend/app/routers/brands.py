"""品牌公开路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.brand import Brand
from app.models.juice import Juice
from app.services.brand import get_brands

router = APIRouter(prefix="/api/brands", tags=["品牌"])


@router.get("")
def list_brands(page: int = 1, size: int = 20, country: str | None = None, session: Session = Depends(get_session)) -> dict:
    """品牌列表，支持分页和按国家筛选"""
    result = get_brands(session, page, size, country)
    return {"code": 0, "message": "ok", "data": result}


@router.get("/{brand_id}")
def get_brand(brand_id: int, session: Session = Depends(get_session)) -> dict:
    """品牌详情"""
    brand = session.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    juice_count = session.exec(select(func.count(Juice.id)).where(Juice.brand_id == brand_id)).one()
    return {
        "code": 0, "message": "ok",
        "data": {
            "id": brand.id, "name": brand.name, "country": brand.country,
            "logo_url": brand.logo_url, "description": brand.description,
            "juice_count": juice_count,
            "created_at": brand.created_at.isoformat() if brand.created_at else "",
        },
    }
