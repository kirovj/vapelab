"""口味标签公开路由"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.flavor_tag import FlavorTag

router = APIRouter(prefix="/api/tags", tags=["标签"])


@router.get("")
def list_tags(session: Session = Depends(get_session)) -> dict:
    """获取全部口味标签"""
    tags = session.exec(select(FlavorTag)).all()
    return {"code": 0, "message": "ok", "data": [{"id": t.id, "name": t.name} for t in tags]}
