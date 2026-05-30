"""口味标签管理后台路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from app.database import get_session
from app.auth.dependencies import get_admin_user
from app.models.user import User
from app.models.flavor_tag import FlavorTag

router = APIRouter(prefix="/api/admin/tags", tags=["管理-标签"])


class TagCreate(BaseModel):
    """创建标签请求"""
    name: str


class TagUpdate(BaseModel):
    """更新标签请求"""
    name: str


@router.post("/create")
def admin_create_tag(data: TagCreate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """新建标签"""
    existing = session.exec(select(FlavorTag).where(FlavorTag.name == data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="标签已存在")
    tag = FlavorTag(name=data.name)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return {"code": 0, "message": "创建成功", "data": {"id": tag.id}}


@router.post("/{tag_id}/update")
def admin_update_tag(tag_id: int, data: TagUpdate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """编辑标签"""
    tag = session.get(FlavorTag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    tag.name = data.name
    session.add(tag)
    session.commit()
    return {"code": 0, "message": "更新成功", "data": None}


@router.post("/{tag_id}/delete")
def admin_delete_tag(tag_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """删除标签"""
    tag = session.get(FlavorTag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    session.delete(tag)
    session.commit()
    return {"code": 0, "message": "删除成功", "data": None}
