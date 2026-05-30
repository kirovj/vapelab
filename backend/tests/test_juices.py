"""测试烟油API"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.models.user import User
from app.auth.jwt import create_access_token
from app.auth.password import hash_password
from app.models.brand import Brand
from app.models.flavor_tag import FlavorTag
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


def _create_brand(session: Session) -> Brand:
    """辅助函数：创建一个测试品牌并返回"""
    brand = Brand(name="测试品牌", country="CN")
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


def _create_tag(session: Session, name: str = "清新") -> FlavorTag:
    """辅助函数：创建一个测试标签并返回"""
    tag = FlavorTag(name=name)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def test_list_juices_empty() -> None:
    """测试空烟油列表"""
    resp = client.get("/api/juices")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["total"] == 0
    assert data["data"]["items"] == []


def test_create_juice(auth_header: dict) -> None:
    """测试创建烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    resp = client.post("/api/admin/juices/create", json={
        "brand_id": brand_id,
        "name": "芒果冰",
        "flavor_profile": "水果",
        "nicotine_range": "3mg",
        "vg_pg_ratio": "70/30",
        "volume": "60ml",
        "price_range": "99-129",
        "description": "清爽芒果味烟油",
    }, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert resp.json()["data"]["id"] is not None


def test_create_juice_with_tags(auth_header: dict) -> None:
    """测试创建带标签的烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        tag = _create_tag(session, "清新")
        brand_id = brand.id
        tag_id = tag.id
    resp = client.post("/api/admin/juices/create", json={
        "brand_id": brand_id,
        "name": "薄荷烟草",
        "tag_ids": [tag_id],
    }, headers=auth_header)
    assert resp.status_code == 200
    juice_id = resp.json()["data"]["id"]
    # 验证详情包含标签
    detail = client.get(f"/api/juices/{juice_id}")
    tags = detail.json()["data"]["tags"]
    assert len(tags) == 1
    assert tags[0]["name"] == "清新"


def test_list_juices_after_create(auth_header: dict) -> None:
    """测试创建后烟油列表"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "芒果冰"}, headers=auth_header)
    resp = client.get("/api/juices")
    assert resp.json()["data"]["total"] == 1
    assert resp.json()["data"]["items"][0]["name"] == "芒果冰"


def test_get_juice_detail(auth_header: dict) -> None:
    """测试烟油详情"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    r = client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "荔枝玫瑰"}, headers=auth_header)
    juice_id = r.json()["data"]["id"]
    resp = client.get(f"/api/juices/{juice_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "荔枝玫瑰"
    assert resp.json()["data"]["brand_id"] == brand_id
    assert resp.json()["data"]["brand_name"] == "测试品牌"


def test_get_juice_not_found() -> None:
    """测试获取不存在的烟油"""
    resp = client.get("/api/juices/99999")
    assert resp.status_code == 404


def test_search_juices(auth_header: dict) -> None:
    """测试搜索烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "芒果冰"}, headers=auth_header)
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "草莓奶昔"}, headers=auth_header)
    # 搜索名称
    resp = client.get("/api/juices/search?q=芒果")
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 1


def test_search_juices_by_brand_name(auth_header: dict) -> None:
    """测试按品牌名搜索烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "经典烟草"}, headers=auth_header)
    # 搜索品牌名
    resp = client.get("/api/juices/search?q=测试品牌")
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 1


def test_top_rated(auth_header: dict) -> None:
    """测试高分排行"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "果汁冰"}, headers=auth_header)
    resp = client.get("/api/juices/top-rated")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) >= 1


def test_update_juice(auth_header: dict) -> None:
    """测试更新烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    r = client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "原名"}, headers=auth_header)
    juice_id = r.json()["data"]["id"]
    resp = client.post(f"/api/admin/juices/{juice_id}/update", json={"name": "新名称"}, headers=auth_header)
    assert resp.status_code == 200
    detail = client.get(f"/api/juices/{juice_id}")
    assert detail.json()["data"]["name"] == "新名称"


def test_update_juice_not_found(auth_header: dict) -> None:
    """测试更新不存在的烟油"""
    resp = client.post("/api/admin/juices/99999/update", json={"name": "新名称"}, headers=auth_header)
    assert resp.status_code == 404


def test_delete_juice(auth_header: dict) -> None:
    """测试删除烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        brand_id = brand.id
    r = client.post("/api/admin/juices/create", json={"brand_id": brand_id, "name": "待删除"}, headers=auth_header)
    juice_id = r.json()["data"]["id"]
    resp = client.post(f"/api/admin/juices/{juice_id}/delete", headers=auth_header)
    assert resp.status_code == 200
    # 验证已删除
    assert client.get(f"/api/juices/{juice_id}").status_code == 404


def test_delete_juice_not_found(auth_header: dict) -> None:
    """测试删除不存在的烟油"""
    resp = client.post("/api/admin/juices/99999/delete", headers=auth_header)
    assert resp.status_code == 404
