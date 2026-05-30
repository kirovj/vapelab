"""文件上传路由"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.utils.image import validate_image, generate_filename, save_image, create_thumbnail

router = APIRouter(prefix="/api/upload", tags=["上传"])


@router.post("")
async def upload_image(file: UploadFile = File(...)) -> dict:
    """上传图片，返回原图和缩略图URL"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    if not validate_image(file.filename):
        raise HTTPException(status_code=400, detail="仅支持 jpg/png/webp 格式")
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过5MB")
    filename = generate_filename(file.filename)
    url = save_image(contents, filename)
    thumb_url = create_thumbnail(contents, filename)
    return {"code": 0, "message": "上传成功", "data": {"url": url, "thumb_url": thumb_url}}
