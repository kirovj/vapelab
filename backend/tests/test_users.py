"""测试用户管理 API"""
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
user_token: str = ""


@pytest.fixture(autouse=True)
def setup_db() -> None:
    """每个测试前重建数据库并创建管理员和普通用户"""
    global admin_token, user_token
    SQLModel.metadata.drop_all(engine)
    init_db()
    with Session(engine) as session:
        admin = User(username="admin", email="admin@test.com", hashed_password=hash_password("123456"), is_admin=True)
        session.add(admin)
        normal = User(username="normal", email="normal@test.com", hashed_password=hash_password("123456"), is_admin=False)
        session.add(normal)
        session.commit()
        admin_token = create_access_token(admin.id)
        user_token = create_access_token(normal.id)


@pytest.fixture
def admin_header() -> dict:
    """管理员认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_header() -> dict:
    """普通用户认证头"""
    return {"Authorization": f"Bearer {user_token}"}


def test_admin_list_users(admin_header: dict) -> None:
    """测试管理员可以获取用户列表"""
    resp = client.get("/api/admin/users", headers=admin_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert len(data["data"]) == 2
    usernames = [u["username"] for u in data["data"]]
    assert "admin" in usernames
    assert "normal" in usernames


def test_non_admin_cannot_list_users(user_header: dict) -> None:
    """测试非管理员无法获取用户列表"""
    resp = client.get("/api/admin/users", headers=user_header)
    assert resp.status_code == 403


def test_admin_toggle_user_active(admin_header: dict) -> None:
    """测试管理员可以禁用/启用用户"""
    # 获取用户列表找到普通用户的 id
    resp = client.get("/api/admin/users", headers=admin_header)
    users = resp.json()["data"]
    normal_user = next(u for u in users if u["username"] == "normal")
    user_id = normal_user["id"]
    assert normal_user["is_active"] is True

    # 禁用
    resp = client.post(f"/api/admin/users/{user_id}/toggle-active", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert "禁用" in resp.json()["message"]

    # 验证已禁用
    resp = client.get("/api/admin/users", headers=admin_header)
    updated = next(u for u in resp.json()["data"] if u["id"] == user_id)
    assert updated["is_active"] is False

    # 再次启用
    resp = client.post(f"/api/admin/users/{user_id}/toggle-active", headers=admin_header)
    assert resp.status_code == 200
    assert "启用" in resp.json()["message"]

    resp = client.get("/api/admin/users", headers=admin_header)
    updated = next(u for u in resp.json()["data"] if u["id"] == user_id)
    assert updated["is_active"] is True


def test_non_admin_cannot_toggle_user(user_header: dict) -> None:
    """测试非管理员无法启用/禁用用户"""
    resp = client.post("/api/admin/users/1/toggle-active", headers=user_header)
    assert resp.status_code == 403


def test_toggle_nonexistent_user(admin_header: dict) -> None:
    """测试切换不存在的用户返回 404"""
    resp = client.post("/api/admin/users/9999/toggle-active", headers=admin_header)
    assert resp.status_code == 404


def test_unauthenticated_cannot_access() -> None:
    """测试未登录用户无法访问"""
    resp = client.get("/api/admin/users")
    assert resp.status_code == 403
    resp = client.post("/api/admin/users/1/toggle-active")
    assert resp.status_code == 403
