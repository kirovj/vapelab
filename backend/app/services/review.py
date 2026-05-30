"""评分评论业务逻辑"""
from sqlmodel import Session, select, func
from app.models.review import Review
from app.models.juice import Juice


def create_review(session: Session, user_id: int, data) -> Review:
    """创建评分评论，并更新烟油平均分和评论数"""
    # 检查是否已评论过
    existing = session.exec(
        select(Review).where(Review.juice_id == data.juice_id).where(Review.user_id == user_id)
    ).first()
    if existing:
        raise ValueError("您已评论过该烟油")

    review = Review(juice_id=data.juice_id, user_id=user_id, rating=data.rating, comment=data.comment)
    session.add(review)
    _update_juice_stats(session, data.juice_id)
    session.commit()
    session.refresh(review)
    return review


def get_reviews_by_juice(session: Session, juice_id: int, page: int = 1, size: int = 20) -> dict:
    """获取烟油的评论列表"""
    from app.models.user import User
    total = session.exec(select(func.count(Review.id)).where(Review.juice_id == juice_id)).one()
    reviews = session.exec(
        select(Review).where(Review.juice_id == juice_id).order_by(Review.created_at.desc()).offset((page - 1) * size).limit(size)
    ).all()
    items = []
    for r in reviews:
        user = session.get(User, r.user_id)
        items.append({
            "id": r.id,
            "juice_id": r.juice_id,
            "user_id": r.user_id,
            "username": user.username if user else "未知用户",
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat() if r.created_at else "",
        })
    return {"items": items, "total": total, "page": page, "size": size}


def update_review(session: Session, review: Review, data) -> Review:
    """更新评论（仅作者可操作）"""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    session.add(review)
    session.commit()
    session.refresh(review)
    _update_juice_stats(session, review.juice_id)
    return review


def delete_review(session: Session, review: Review) -> None:
    """删除评论"""
    juice_id = review.juice_id
    session.delete(review)
    session.commit()
    _update_juice_stats(session, juice_id)


def _update_juice_stats(session: Session, juice_id: int) -> None:
    """更新烟油的平均评分和评论数"""
    juice = session.get(Juice, juice_id)
    if not juice:
        return
    result = session.exec(
        select(func.count(Review.id), func.avg(Review.rating)).where(Review.juice_id == juice_id)
    ).one()
    count, avg = result
    juice.review_count = count or 0
    juice.avg_rating = round(float(avg) if avg else 0.0, 1)
    session.add(juice)
    session.commit()
