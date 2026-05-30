"""烟油管理后台路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.auth.dependencies import get_admin_user
from app.models.user import User
from app.models.juice import Juice
from app.schemas.juice import JuiceCreate, JuiceUpdate
from app.services.juice import create_juice, update_juice, delete_juice

router = APIRouter(prefix="/api/admin/juices", tags=["管理-烟油"])


@router.post("/create")
def admin_create_juice(data: JuiceCreate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """新建烟油"""
    juice = create_juice(session, data)
    return {"code": 0, "message": "创建成功", "data": {"id": juice.id}}


@router.post("/{juice_id}/update")
def admin_update_juice(juice_id: int, data: JuiceUpdate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """编辑烟油"""
    juice = session.get(Juice, juice_id)
    if not juice:
        raise HTTPException(status_code=404, detail="烟油不存在")
    update_juice(session, juice, data)
    return {"code": 0, "message": "更新成功", "data": None}


@router.post("/{juice_id}/delete")
def admin_delete_juice(juice_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """删除烟油"""
    juice = session.get(Juice, juice_id)
    if not juice:
        raise HTTPException(status_code=404, detail="烟油不存在")
    delete_juice(session, juice)
    return {"code": 0, "message": "删除成功", "data": None}
