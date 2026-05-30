"""测试用户提交和审核 API"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.models.user import User
from app.auth.jwt import create_access_token
from app.auth.password import hash_password
from app.models.brand import Brand
from app.models.juice import Juice, JuiceStatus
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
        normal = User(username="user", email="user@test.com", hashed_password=hash_password("123456"), is_admin=False)
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


def _create_brand(session: Session) -> Brand:
    """辅助函数：创建一个测试品牌并返回"""
    brand = Brand(name="测试品牌", country="CN")
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


def test_submit_juice_without_auth() -> None:
    """未登录用户提交烟油应返回403"""
    resp = client.post("/api/submissions/create", json={
        "brand_id": 1,
        "name": "芒果冰",
    })
    assert resp.status_code == 403


def test_submit_juice_success(user_header: dict) -> None:
    """测试用户提交烟油成功"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    resp = client.post("/api/submissions/create", json={
        "brand_id": brand_id,
        "name": "芒果冰",
        "flavor_profile": "水果",
        "nicotine_range": "3mg",
        "vg_pg_ratio": "70/30",
        "volume": "60ml",
        "price_range": "99-129",
        "description": "清爽芒果味烟油",
    }, headers=user_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["message"] == "提交成功，等待审核"
    assert data["data"]["id"] is not None


def test_submit_juice_status_pending(user_header: dict) -> None:
    """测试提交的烟油状态为 PENDING"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    resp = client.post("/api/submissions/create", json={
        "brand_id": brand_id,
        "name": "草莓奶昔",
    }, headers=user_header)
    juice_id = resp.json()["data"]["id"]
    # 验证详情页的状态
    detail = client.get(f"/api/juices/{juice_id}")
    assert detail.json()["data"]["status"] == JuiceStatus.PENDING.value


def test_my_submissions(user_header: dict) -> None:
    """测试获取我的提交记录"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    # 先提交两个烟油
    client.post("/api/submissions/create", json={"brand_id": brand_id, "name": "芒果冰"}, headers=user_header)
    client.post("/api/submissions/create", json={"brand_id": brand_id, "name": "草莓奶昔"}, headers=user_header)
    resp = client.get("/api/submissions/my", headers=user_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert len(data["data"]) == 2


def test_my_submissions_require_auth() -> None:
    """未登录用户访问我的提交应返回403"""
    resp = client.get("/api/submissions/my")
    assert resp.status_code == 403


def test_admin_list_pending_submissions(admin_header: dict, user_header: dict) -> None:
    """测试管理员查看待审核列表"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    # 用户提交一个烟油
    client.post("/api/submissions/create", json={"brand_id": brand_id, "name": "芒果冰"}, headers=user_header)
    # 管理员直接创建一个已发布的烟油（不应该出现在待审核列表）
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "已发布烟油"}, headers=admin_header)
    resp = client.get("/api/admin/submissions", headers=admin_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    # 待审核列表应该只有用户提交的那个
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "芒果冰"
    assert data["data"][0]["status"] == JuiceStatus.PENDING.value


def test_admin_approve_submission(admin_header: dict, user_header: dict) -> None:
    """测试管理员审核通过"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    resp = client.post("/api/submissions/create", json={"brand_id": brand_id, "name": "芒果冰"}, headers=user_header)
    juice_id = resp.json()["data"]["id"]
    # 管理员审核通过
    resp = client.post(f"/api/admin/submissions/{juice_id}/approve", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["message"] == "审核通过"
    # 验证状态已变为 PUBLISHED
    detail = client.get(f"/api/juices/{juice_id}")
    assert detail.json()["data"]["status"] == JuiceStatus.PUBLISHED.value


def test_admin_reject_submission(admin_header: dict, user_header: dict) -> None:
    """测试管理员审核拒绝"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    resp = client.post("/api/submissions/create", json={"brand_id": brand_id, "name": "问题烟油"}, headers=user_header)
    juice_id = resp.json()["data"]["id"]
    # 管理员审核拒绝
    resp = client.post(f"/api/admin/submissions/{juice_id}/reject", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["message"] == "已拒绝"
    # 验证状态已变为 ARCHIVED
    detail = client.get(f"/api/juices/{juice_id}")
    assert detail.json()["data"]["status"] == JuiceStatus.ARCHIVED.value


def test_approve_not_found(admin_header: dict) -> None:
    """测试审核不存在的烟油"""
    resp = client.post("/api/admin/submissions/99999/approve", headers=admin_header)
    assert resp.status_code == 404


def test_reject_not_found(admin_header: dict) -> None:
    """测试拒绝不存在的烟油"""
    resp = client.post("/api/admin/submissions/99999/reject", headers=admin_header)
    assert resp.status_code == 404


def test_non_admin_cannot_list_submissions(user_header: dict) -> None:
    """非管理员不能查看待审核列表"""
    resp = client.get("/api/admin/submissions", headers=user_header)
    assert resp.status_code == 403


def test_non_admin_cannot_approve(user_header: dict) -> None:
    """非管理员不能审核通过"""
    resp = client.post("/api/admin/submissions/1/approve", headers=user_header)
    assert resp.status_code == 403


def test_non_admin_cannot_reject(user_header: dict) -> None:
    """非管理员不能审核拒绝"""
    resp = client.post("/api/admin/submissions/1/reject", headers=user_header)
    assert resp.status_code == 403
