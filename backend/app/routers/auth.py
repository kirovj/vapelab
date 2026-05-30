"""认证路由：注册、登录"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(req: RegisterRequest, session: Session = Depends(get_session)) -> dict:
    """用户注册"""
    existing = session.exec(
        select(User).where((User.username == req.username) | (User.email == req.email))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    user = User(
        username=req.username,
        email=req.email,
        hashed_password=hash_password(req.password),
    )
    session.add(user)
    session.commit()
    return {"code": 0, "message": "注册成功", "data": None}


@router.post("/login")
def login(req: LoginRequest, session: Session = Depends(get_session)) -> dict:
    """用户登录"""
    user = session.exec(
        select(User).where(
            (User.username == req.username) | (User.email == req.username)
        )
    ).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    return {
        "code": 0,
        "message": "登录成功",
        "data": {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            },
        },
    }
