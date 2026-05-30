"""用户资料路由"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from app.database import get_session
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["用户"])


class UserUpdate(BaseModel):
    """用户资料更新请求"""
    username: str | None = None
    email: str | None = None


@router.get("/me")
def get_me(user: User = Depends(get_current_user)) -> dict:
    """获取当前登录用户信息"""
    return {
        "code": 0,
        "message": "ok",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
        },
    }


@router.post("/me/update")
def update_me(
    data: UserUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    """更新当前登录用户资料"""
    if data.username is not None:
        user.username = data.username
    if data.email is not None:
        user.email = data.email
    session.add(user)
    session.commit()
    return {"code": 0, "message": "更新成功", "data": None}
