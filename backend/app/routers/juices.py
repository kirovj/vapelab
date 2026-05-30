"""烟油公开路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.database import get_session
from app.services.juice import get_juices, search_juices, get_top_rated, _juice_to_dict

router = APIRouter(prefix="/api/juices", tags=["烟油"])


@router.get("")
def list_juices(
    page: int = 1, size: int = 20,
    brand_id: int | None = None,
    flavor_profile: str | None = None,
    sort: str = "newest",
    session: Session = Depends(get_session),
) -> dict:
    """烟油列表，支持筛选排序"""
    result = get_juices(session, page, size, brand_id, flavor_profile, None, sort)
    return {"code": 0, "message": "ok", "data": result}


@router.get("/search")
def search(q: str = Query(...), page: int = 1, size: int = 20, session: Session = Depends(get_session)) -> dict:
    """全文搜索烟油"""
    result = search_juices(session, q, page, size)
    return {"code": 0, "message": "ok", "data": result}


@router.get("/top-rated")
def top_rated(limit: int = 20, session: Session = Depends(get_session)) -> dict:
    """高分排行"""
    juices = get_top_rated(session, limit)
    return {"code": 0, "message": "ok", "data": juices}


@router.get("/{juice_id}")
def get_juice(juice_id: int, session: Session = Depends(get_session)) -> dict:
    """烟油详情"""
    from app.models.juice import Juice
    juice = session.get(Juice, juice_id)
    if not juice:
        raise HTTPException(status_code=404, detail="烟油不存在")
    return {"code": 0, "message": "ok", "data": _juice_to_dict(session, juice)}
