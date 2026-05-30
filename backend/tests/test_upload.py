"""测试图片上传"""
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_image() -> io.BytesIO:
    """创建测试用PNG图片"""
    from PIL import Image
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def test_upload_valid_image() -> None:
    """测试上传有效图片"""
    img = create_test_image()
    resp = client.post("/api/upload", files={"file": ("test.png", img, "image/png")})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["url"].startswith("/static/uploads/")
    assert data["thumb_url"].startswith("/static/uploads/thumbs/")


def test_upload_invalid_extension() -> None:
    """测试上传无效格式"""
    resp = client.post("/api/upload", files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")})
    assert resp.status_code == 400


def test_upload_empty_filename() -> None:
    """测试空文件名（FastAPI 表单验证会返回 422）"""
    resp = client.post("/api/upload", files={"file": ("", io.BytesIO(b""), "image/png")})
    assert resp.status_code == 422
