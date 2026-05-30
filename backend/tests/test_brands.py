"""测试品牌API"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.models.user import User
from app.auth.jwt import create_access_token
from app.auth.password import hash_password
from sqlmodel import SQLModel, Session

client = TestClient(app)

admin_token: str = ""


@pytest.fixture(autouse=True)
def setup_db() -> None:
    """每个测试前重建数据库并创建管理员"""
    global admin_token
    SQLModel.metadata.drop_all(engine)
    init_db()
    with Session(engine) as session:
        admin = User(username="admin", email="admin@test.com", hashed_password=hash_password("123456"), is_admin=True)
        session.add(admin)
        session.commit()
        admin_token = create_access_token(admin.id)


@pytest.fixture
def auth_header() -> dict:
    """管理员认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


def test_list_brands_empty() -> None:
    """测试空品牌列表"""
    resp = client.get("/api/brands")
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 0


def test_create_brand(auth_header: dict) -> None:
    """测试创建品牌"""
    resp = client.post("/api/admin/brands/create", json={"name": "Test Brand", "country": "USA"}, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_list_brands_after_create(auth_header: dict) -> None:
    """测试创建后品牌列表"""
    client.post("/api/admin/brands/create", json={"name": "Brand A", "country": "USA"}, headers=auth_header)
    resp = client.get("/api/brands")
    assert resp.json()["data"]["total"] == 1


def test_get_brand_detail(auth_header: dict) -> None:
    """测试品牌详情"""
    r = client.post("/api/admin/brands/create", json={"name": "Brand X", "country": "CN"}, headers=auth_header)
    brand_id = r.json()["data"]["id"]
    resp = client.get(f"/api/brands/{brand_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Brand X"


def test_update_brand(auth_header: dict) -> None:
    """测试更新品牌"""
    r = client.post("/api/admin/brands/create", json={"name": "Old Name", "country": "JP"}, headers=auth_header)
    brand_id = r.json()["data"]["id"]
    resp = client.post(f"/api/admin/brands/{brand_id}/update", json={"name": "New Name"}, headers=auth_header)
    assert resp.status_code == 200
    detail = client.get(f"/api/brands/{brand_id}")
    assert detail.json()["data"]["name"] == "New Name"


def test_delete_brand(auth_header: dict) -> None:
    """测试删除品牌"""
    r = client.post("/api/admin/brands/create", json={"name": "To Delete", "country": "UK"}, headers=auth_header)
    brand_id = r.json()["data"]["id"]
    resp = client.post(f"/api/admin/brands/{brand_id}/delete", headers=auth_header)
    assert resp.status_code == 200
    # 验证已删除
    assert client.get(f"/api/brands/{brand_id}").status_code == 404
