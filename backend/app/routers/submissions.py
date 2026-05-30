"""用户提交路由"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.juice import Juice, JuiceStatus
from app.schemas.juice import JuiceCreate
from app.services.juice import create_juice, _juice_to_dict

router = APIRouter(prefix="/api/submissions", tags=["提交"])


@router.post("/create")
def submit_juice(data: JuiceCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> dict:
    """用户提交新烟油数据"""
    juice = create_juice(session, data)
    juice.status = JuiceStatus.PENDING
    juice.submitted_by = user.id
    session.add(juice)
    session.commit()
    session.refresh(juice)
    return {"code": 0, "message": "提交成功，等待审核", "data": {"id": juice.id}}


@router.get("/my")
def my_submissions(session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> dict:
    """我的提交记录"""
    juices = session.exec(
        select(Juice).where(Juice.submitted_by == user.id).order_by(Juice.created_at.desc())
    ).all()
    items = [_juice_to_dict(session, j) for j in juices]
    return {"code": 0, "message": "ok", "data": items}
