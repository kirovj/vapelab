"""品牌管理后台路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.auth.dependencies import get_admin_user
from app.models.user import User
from app.schemas.brand import BrandCreate, BrandUpdate
from app.services.brand import get_brand_by_id, create_brand, update_brand, delete_brand

router = APIRouter(prefix="/api/admin/brands", tags=["管理-品牌"])


@router.post("/create")
def admin_create_brand(data: BrandCreate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """新建品牌"""
    brand = create_brand(session, data)
    return {"code": 0, "message": "创建成功", "data": {"id": brand.id}}


@router.post("/{brand_id}/update")
def admin_update_brand(brand_id: int, data: BrandUpdate, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """编辑品牌"""
    brand = get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    update_brand(session, brand, data)
    return {"code": 0, "message": "更新成功", "data": None}


@router.post("/{brand_id}/delete")
def admin_delete_brand(brand_id: int, session: Session = Depends(get_session), admin: User = Depends(get_admin_user)) -> dict:
    """删除品牌"""
    brand = get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    delete_brand(session, brand)
    return {"code": 0, "message": "删除成功", "data": None}
