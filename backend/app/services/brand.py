"""品牌业务逻辑"""
from sqlmodel import Session, select, func
from app.models.brand import Brand
from app.models.juice import Juice
from app.utils.cache import brand_cache


def get_brands(session: Session, page: int = 1, size: int = 20, country: str | None = None) -> dict:
    """获取品牌列表，支持分页和按国家筛选（无筛选时使用缓存）"""
    cache_key = f"brands:{page}:{size}:{country or 'all'}"
    if cache_key in brand_cache:
        return brand_cache[cache_key]

    query = select(Brand)
    count_query = select(func.count(Brand.id))
    if country:
        query = query.where(Brand.country == country)
        count_query = count_query.where(Brand.country == country)
    total = session.exec(count_query).one()
    brands = session.exec(query.offset((page - 1) * size).limit(size)).all()
    items = []
    for b in brands:
        juice_count = session.exec(select(func.count(Juice.id)).where(Juice.brand_id == b.id)).one()
        items.append({
            "id": b.id, "name": b.name, "country": b.country,
            "logo_url": b.logo_url, "description": b.description,
            "juice_count": juice_count,
            "created_at": b.created_at.isoformat() if b.created_at else "",
        })
    result = {"items": items, "total": total, "page": page, "size": size}
    brand_cache[cache_key] = result
    return result


def _invalidate_brand_cache() -> None:
    """清除品牌缓存"""
    brand_cache.clear()


def get_brand_by_id(session: Session, brand_id: int) -> Brand | None:
    """根据ID获取品牌"""
    return session.get(Brand, brand_id)


def create_brand(session: Session, data) -> Brand:
    """创建品牌"""
    brand = Brand(**data.model_dump())
    session.add(brand)
    session.commit()
    session.refresh(brand)
    _invalidate_brand_cache()
    return brand


def update_brand(session: Session, brand: Brand, data) -> Brand:
    """更新品牌"""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(brand, key, value)
    session.add(brand)
    session.commit()
    session.refresh(brand)
    _invalidate_brand_cache()
    return brand


def delete_brand(session: Session, brand: Brand) -> None:
    """删除品牌及关联烟油"""
    juices = session.exec(select(Juice).where(Juice.brand_id == brand.id)).all()
    for juice in juices:
        session.delete(juice)
    session.delete(brand)
    session.commit()
    _invalidate_brand_cache()
