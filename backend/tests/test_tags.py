"""测试口味标签API"""
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


def test_list_tags_empty() -> None:
    """测试空标签列表"""
    resp = client.get("/api/tags")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_create_tag(auth_header: dict) -> None:
    """测试创建标签"""
    resp = client.post("/api/admin/tags/create", json={"name": "清新"}, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_list_tags_after_create(auth_header: dict) -> None:
    """测试创建后标签列表"""
    client.post("/api/admin/tags/create", json={"name": "清新"}, headers=auth_header)
    client.post("/api/admin/tags/create", json={"name": "浓郁"}, headers=auth_header)
    resp = client.get("/api/tags")
    assert len(resp.json()["data"]) == 2


def test_create_duplicate_tag(auth_header: dict) -> None:
    """测试重复创建标签"""
    client.post("/api/admin/tags/create", json={"name": "清新"}, headers=auth_header)
    resp = client.post("/api/admin/tags/create", json={"name": "清新"}, headers=auth_header)
    assert resp.status_code == 400


def test_delete_tag(auth_header: dict) -> None:
    """测试删除标签"""
    r = client.post("/api/admin/tags/create", json={"name": "待删除"}, headers=auth_header)
    tag_id = r.json()["data"]["id"]
    resp = client.post(f"/api/admin/tags/{tag_id}/delete", headers=auth_header)
    assert resp.status_code == 200
    assert client.get("/api/tags").json()["data"] == []
