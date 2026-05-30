"""用户管理后台路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.auth.dependencies import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/api/admin/users", tags=["管理-用户"])


@router.get("")
def list_users(session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """用户列表"""
    users = session.exec(select(User).order_by(User.created_at.desc())).all()
    items = [{"id": u.id, "username": u.username, "email": u.email, "is_admin": u.is_admin, "is_active": u.is_active, "created_at": u.created_at.isoformat() if u.created_at else ""} for u in users]
    return {"code": 0, "message": "ok", "data": items}


@router.post("/{user_id}/toggle-active")
def toggle_active(user_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """启用/禁用用户"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = not user.is_active
    session.add(user)
    session.commit()
    status_text = "启用" if user.is_active else "禁用"
    return {"code": 0, "message": f"已{status_text}", "data": None}
