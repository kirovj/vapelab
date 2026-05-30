"""测试评分评论API"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.models.user import User
from app.models.brand import Brand
from app.models.juice import Juice
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
        user = User(username="testuser", email="user@test.com", hashed_password=hash_password("123456"))
        session.add(user)
        session.commit()
        admin_token = create_access_token(admin.id)
        user_token = create_access_token(user.id)


@pytest.fixture
def admin_auth() -> dict:
    """管理员认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_auth() -> dict:
    """普通用户认证头"""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def another_user_auth() -> dict:
    """另一个普通用户认证头"""
    with Session(engine) as session:
        other = User(username="other", email="other@test.com", hashed_password=hash_password("123456"))
        session.add(other)
        session.commit()
        token = create_access_token(other.id)
    return {"Authorization": f"Bearer {token}"}


def _create_brand(session: Session) -> Brand:
    """辅助函数：创建一个测试品牌并返回"""
    brand = Brand(name="测试品牌", country="CN")
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


def _create_juice(session: Session, brand_id: int, name: str = "芒果冰") -> Juice:
    """辅助函数：创建一个测试烟油并返回"""
    juice = Juice(brand_id=brand_id, name=name, status="published")
    session.add(juice)
    session.commit()
    session.refresh(juice)
    return juice


def test_list_reviews_empty() -> None:
    """测试空评论列表"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    resp = client.get(f"/api/juices/{juice_id}/reviews")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["total"] == 0
    assert data["data"]["items"] == []


def test_create_review(user_auth: dict) -> None:
    """测试创建评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    resp = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
        "comment": "非常好抽",
    }, headers=user_auth)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert resp.json()["data"]["id"] is not None


def test_create_review_without_comment(user_auth: dict) -> None:
    """测试创建无文字评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    resp = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 7,
    }, headers=user_auth)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_create_review_without_auth() -> None:
    """测试未登录创建评论应返回403"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    resp = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
        "comment": "不错",
    })
    assert resp.status_code == 403


def test_cannot_review_twice(user_auth: dict) -> None:
    """测试不能重复评论同一烟油"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    # 第一次评论
    resp = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 9,
        "comment": "很棒",
    }, headers=user_auth)
    assert resp.status_code == 200
    # 第二次评论同一烟油
    resp = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 6,
        "comment": "一般般",
    }, headers=user_auth)
    assert resp.status_code == 400


def test_update_own_review(user_auth: dict) -> None:
    """测试修改自己的评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    # 创建评论
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 5,
        "comment": "一般",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # 修改评论
    resp = client.post(f"/api/reviews/{review_id}/update", json={
        "rating": 9,
        "comment": "真香",
    }, headers=user_auth)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    # 验证列表中的评论已更新
    reviews = client.get(f"/api/juices/{juice_id}/reviews").json()
    assert reviews["data"]["items"][0]["rating"] == 9
    assert reviews["data"]["items"][0]["comment"] == "真香"


def test_update_review_partial(user_auth: dict) -> None:
    """测试部分更新评论（仅修改评分）"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 5,
        "comment": "还行",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # 仅修改评分
    resp = client.post(f"/api/reviews/{review_id}/update", json={
        "rating": 10,
    }, headers=user_auth)
    assert resp.status_code == 200
    reviews = client.get(f"/api/juices/{juice_id}/reviews").json()
    assert reviews["data"]["items"][0]["rating"] == 10
    assert reviews["data"]["items"][0]["comment"] == "还行"


def test_cannot_update_others_review(user_auth: dict, another_user_auth: dict) -> None:
    """测试不能修改他人的评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
        "comment": "user 的评论",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # other 用户尝试修改
    resp = client.post(f"/api/reviews/{review_id}/update", json={
        "rating": 1,
    }, headers=another_user_auth)
    assert resp.status_code == 403


def test_delete_own_review(user_auth: dict) -> None:
    """测试删除自己的评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 7,
        "comment": "还不错",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # 删除
    resp = client.post(f"/api/reviews/{review_id}/delete", headers=user_auth)
    assert resp.status_code == 200
    # 验证列表为空
    reviews = client.get(f"/api/juices/{juice_id}/reviews").json()
    assert reviews["data"]["total"] == 0


def test_cannot_delete_others_review(user_auth: dict, another_user_auth: dict) -> None:
    """测试不能删除他人的评论"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
        "comment": "user 的评论",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # other 用户尝试删除
    resp = client.post(f"/api/reviews/{review_id}/delete", headers=another_user_auth)
    assert resp.status_code == 403


def test_update_review_not_found(user_auth: dict) -> None:
    """测试修改不存在的评论"""
    resp = client.post("/api/reviews/99999/update", json={"rating": 5}, headers=user_auth)
    assert resp.status_code == 404


def test_delete_review_not_found(user_auth: dict) -> None:
    """测试删除不存在的评论"""
    resp = client.post("/api/reviews/99999/delete", headers=user_auth)
    assert resp.status_code == 404


def test_review_updates_juice_stats(user_auth: dict) -> None:
    """测试评论影响烟油评分统计"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    # 创建评论
    client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
        "comment": "好",
    }, headers=user_auth)
    # 验证烟油统计
    detail = client.get(f"/api/juices/{juice_id}").json()
    assert detail["data"]["review_count"] == 1
    assert detail["data"]["avg_rating"] == 8.0


def test_delete_review_updates_juice_stats(user_auth: dict) -> None:
    """测试删除评论后烟油统计更新"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    r = client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 6,
        "comment": "还行",
    }, headers=user_auth)
    review_id = r.json()["data"]["id"]
    # 删除评论
    client.post(f"/api/reviews/{review_id}/delete", headers=user_auth)
    # 验证统计归零
    detail = client.get(f"/api/juices/{juice_id}").json()
    assert detail["data"]["review_count"] == 0
    assert detail["data"]["avg_rating"] == 0.0


def test_list_reviews_pagination(user_auth: dict) -> None:
    """测试评论列表分页"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    # 创建多条评论（用同一个用户只能创建一条，需要不同用户）
    with Session(engine) as session:
        for i in range(3):
            u = User(username=f"reviewer{i}", email=f"r{i}@test.com", hashed_password=hash_password("123456"))
            session.add(u)
            session.commit()
            token = create_access_token(u.id)
            client.post("/api/reviews/create", json={
                "juice_id": juice_id,
                "rating": 5 + i,
                "comment": f"评论{i}",
            }, headers={"Authorization": f"Bearer {token}"})
    # 测试分页
    resp = client.get(f"/api/juices/{juice_id}/reviews?page=1&size=2")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["size"] == 2


def test_create_review_updates_juice_avg_rating_with_multiple(user_auth: dict) -> None:
    """测试多个评论评分取平均值"""
    with Session(engine) as session:
        brand = _create_brand(session)
        juice = _create_juice(session, brand.id)
        juice_id = juice.id
    # user 评分 8
    client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 8,
    }, headers=user_auth)
    # another user 评分 4
    with Session(engine) as session:
        u2 = User(username="reviewer2", email="r2@test.com", hashed_password=hash_password("123456"))
        session.add(u2)
        session.commit()
        token2 = create_access_token(u2.id)
    client.post("/api/reviews/create", json={
        "juice_id": juice_id,
        "rating": 4,
    }, headers={"Authorization": f"Bearer {token2}"})
    # 平均分应为 6.0
    detail = client.get(f"/api/juices/{juice_id}").json()
    assert detail["data"]["review_count"] == 2
    assert detail["data"]["avg_rating"] == 6.0
