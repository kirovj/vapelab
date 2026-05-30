"""审核管理后台路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.auth.dependencies import get_admin_user
from app.models.user import User
from app.models.juice import Juice, JuiceStatus
from app.services.juice import _juice_to_dict

router = APIRouter(prefix="/api/admin/submissions", tags=["管理-审核"])


@router.get("")
def list_submissions(session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """待审核列表"""
    juices = session.exec(
        select(Juice).where(Juice.status == JuiceStatus.PENDING).order_by(Juice.created_at.desc())
    ).all()
    items = [_juice_to_dict(session, j) for j in juices]
    return {"code": 0, "message": "ok", "data": items}


@router.post("/{juice_id}/approve")
def approve(juice_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """审核通过"""
    juice = session.get(Juice, juice_id)
    if not juice:
        raise HTTPException(status_code=404, detail="烟油不存在")
    juice.status = JuiceStatus.PUBLISHED
    session.add(juice)
    session.commit()
    return {"code": 0, "message": "审核通过", "data": None}


@router.post("/{juice_id}/reject")
def reject(juice_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """审核拒绝"""
    juice = session.get(Juice, juice_id)
    if not juice:
        raise HTTPException(status_code=404, detail="烟油不存在")
    juice.status = JuiceStatus.ARCHIVED
    session.add(juice)
    session.commit()
    return {"code": 0, "message": "已拒绝", "data": None}
