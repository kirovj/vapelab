"""烟油业务逻辑"""
from sqlmodel import Session, select, func
from app.models.juice import Juice, JuiceStatus
from app.models.brand import Brand
from app.models.flavor_tag import FlavorTag, JuiceFlavorTag


def get_juices(
    session: Session,
    page: int = 1,
    size: int = 20,
    brand_id: int | None = None,
    flavor_profile: str | None = None,
    status: str | None = None,
    sort: str = "newest",
) -> dict:
    """获取烟油列表，支持多条件筛选和排序"""
    query = select(Juice)
    count_query = select(func.count(Juice.id))

    if brand_id:
        query = query.where(Juice.brand_id == brand_id)
        count_query = count_query.where(Juice.brand_id == brand_id)
    if flavor_profile:
        query = query.where(Juice.flavor_profile == flavor_profile)
        count_query = count_query.where(Juice.flavor_profile == flavor_profile)
    if status:
        query = query.where(Juice.status == status)
        count_query = count_query.where(Juice.status == status)
    else:
        query = query.where(Juice.status == JuiceStatus.PUBLISHED)
        count_query = count_query.where(Juice.status == JuiceStatus.PUBLISHED)

    if sort == "rating_desc":
        query = query.order_by(Juice.avg_rating.desc())
    elif sort == "rating_asc":
        query = query.order_by(Juice.avg_rating.asc())
    elif sort == "oldest":
        query = query.order_by(Juice.created_at.asc())
    else:
        query = query.order_by(Juice.created_at.desc())

    total = session.exec(count_query).one()
    juices = session.exec(query.offset((page - 1) * size).limit(size)).all()

    items = []
    for j in juices:
        items.append(_juice_to_dict(session, j))

    return {"items": items, "total": total, "page": page, "size": size}


def search_juices(session: Session, q: str, page: int = 1, size: int = 20) -> dict:
    """全文搜索烟油（按名称、品牌名、描述）"""
    query = select(Juice).join(Brand).where(
        (Juice.name.contains(q)) | (Brand.name.contains(q)) | (Juice.description.contains(q))
    ).where(Juice.status == JuiceStatus.PUBLISHED)
    count_query = select(func.count(Juice.id)).join(Brand).where(
        (Juice.name.contains(q)) | (Brand.name.contains(q)) | (Juice.description.contains(q))
    ).where(Juice.status == JuiceStatus.PUBLISHED)

    total = session.exec(count_query).one()
    juices = session.exec(query.offset((page - 1) * size).limit(size)).all()

    items = [_juice_to_dict(session, j) for j in juices]
    return {"items": items, "total": total, "page": page, "size": size}


def get_top_rated(session: Session, limit: int = 20) -> list[dict]:
    """获取高分排行"""
    juices = session.exec(
        select(Juice).where(Juice.status == JuiceStatus.PUBLISHED).order_by(Juice.avg_rating.desc()).limit(limit)
    ).all()
    return [_juice_to_dict(session, j) for j in juices]


def create_juice(session: Session, data) -> Juice:
    """创建烟油"""
    juice = Juice(**data.model_dump(exclude={"tag_ids"}), status=JuiceStatus.PUBLISHED)
    session.add(juice)
    session.commit()
    session.refresh(juice)
    # 设置标签关联
    _set_tags(session, juice, data.tag_ids)
    return juice


def update_juice(session: Session, juice: Juice, data) -> Juice:
    """更新烟油"""
    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)
    for key, value in update_data.items():
        setattr(juice, key, value)
    session.add(juice)
    session.commit()
    session.refresh(juice)
    if tag_ids is not None:
        _set_tags(session, juice, tag_ids)
    return juice


def delete_juice(session: Session, juice: Juice) -> None:
    """删除烟油及关联"""
    session.exec(select(JuiceFlavorTag).where(JuiceFlavorTag.juice_id == juice.id)).all()
    session.delete(juice)
    session.commit()


def _juice_to_dict(session: Session, juice: Juice) -> dict:
    """将烟油模型转为字典（含品牌名和标签）"""
    tags = session.exec(
        select(FlavorTag).join(JuiceFlavorTag).where(JuiceFlavorTag.juice_id == juice.id)
    ).all()
    brand = session.get(Brand, juice.brand_id)
    return {
        "id": juice.id,
        "brand_id": juice.brand_id,
        "brand_name": brand.name if brand else "",
        "name": juice.name,
        "flavor_profile": juice.flavor_profile,
        "nicotine_range": juice.nicotine_range,
        "vg_pg_ratio": juice.vg_pg_ratio,
        "volume": juice.volume,
        "price_range": juice.price_range,
        "description": juice.description,
        "image_urls": juice.image_urls,
        "status": juice.status.value if juice.status else "",
        "avg_rating": juice.avg_rating,
        "review_count": juice.review_count,
        "tags": [{"id": t.id, "name": t.name} for t in tags],
        "created_at": juice.created_at.isoformat() if juice.created_at else "",
    }


def _set_tags(session: Session, juice: Juice, tag_ids: list[int]) -> None:
    """设置烟油的标签关联"""
    session.exec(select(JuiceFlavorTag).where(JuiceFlavorTag.juice_id == juice.id)).all()
    session.flush()
    for jft in session.exec(select(JuiceFlavorTag).where(JuiceFlavorTag.juice_id == juice.id)).all():
        session.delete(jft)
    session.flush()
    for tag_id in tag_ids:
        jft = JuiceFlavorTag(juice_id=juice.id, tag_id=tag_id)
        session.add(jft)
    session.commit()
