"""评分评论路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.services.review import create_review, get_reviews_by_juice, update_review, delete_review

router = APIRouter(prefix="/api", tags=["评论"])


@router.get("/juices/{juice_id}/reviews")
def list_reviews(juice_id: int, page: int = 1, size: int = 20, session: Session = Depends(get_session)) -> dict:
    """某烟油的评论列表"""
    result = get_reviews_by_juice(session, juice_id, page, size)
    return {"code": 0, "message": "ok", "data": result}


@router.post("/reviews/create")
def create(data: ReviewCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> dict:
    """发表评分评论"""
    try:
        review = create_review(session, user.id, data)
        return {"code": 0, "message": "评论成功", "data": {"id": review.id}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{review_id}/update")
def update(review_id: int, data: ReviewUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> dict:
    """修改自己的评论"""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="只能修改自己的评论")
    update_review(session, review, data)
    return {"code": 0, "message": "更新成功", "data": None}


@router.post("/reviews/{review_id}/delete")
def delete(review_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> dict:
    """删除自己的评论"""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="只能删除自己的评论")
    delete_review(session, review)
    return {"code": 0, "message": "删除成功", "data": None}
