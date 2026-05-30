"""测试认证模块"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from sqlmodel import SQLModel

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db() -> None:
    """每个测试前重建数据库"""
    SQLModel.metadata.drop_all(engine)
    init_db()


def test_register_success() -> None:
    """测试注册成功"""
    resp = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456",
    })
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_register_duplicate() -> None:
    """测试重复注册"""
    client.post("/api/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "123456",
    })
    resp = client.post("/api/auth/register", json={
        "username": "testuser", "email": "test2@test.com", "password": "123456",
    })
    assert resp.status_code == 400


def test_login_success() -> None:
    """测试登录成功"""
    client.post("/api/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "123456",
    })
    resp = client.post("/api/auth/login", json={
        "username": "testuser", "password": "123456",
    })
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "access_token" in data
    assert data["user"]["username"] == "testuser"


def test_login_wrong_password() -> None:
    """测试密码错误"""
    client.post("/api/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "123456",
    })
    resp = client.post("/api/auth/login", json={
        "username": "testuser", "password": "wrong",
    })
    assert resp.status_code == 401


def test_login_by_email() -> None:
    """测试使用邮箱登录"""
    client.post("/api/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "123456",
    })
    resp = client.post("/api/auth/login", json={
        "username": "test@test.com", "password": "123456",
    })
    assert resp.status_code == 200
