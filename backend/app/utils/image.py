"""图片处理工具"""
import os
import uuid
from pathlib import Path
from PIL import Image
from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
THUMBNAIL_SIZE = (300, 300)


def validate_image(filename: str) -> bool:
    """校验文件扩展名是否在白名单中"""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def generate_filename(original_filename: str) -> str:
    """生成随机文件名"""
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"


def save_image(file_data: bytes, filename: str) -> str:
    """保存原图并返回访问路径"""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / filename
    with open(filepath, "wb") as f:
        f.write(file_data)
    return f"/static/uploads/{filename}"


def create_thumbnail(file_data: bytes, filename: str) -> str | None:
    """创建缩略图，返回缩略图路径"""
    try:
        img = Image.open(__import__("io").BytesIO(file_data))
        img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
        thumb_dir = Path(settings.UPLOAD_DIR) / "thumbs"
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / filename
        img.save(thumb_path)
        return f"/static/uploads/thumbs/{filename}"
    except Exception:
        return None
