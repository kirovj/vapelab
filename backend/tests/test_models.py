"""测试数据模型创建"""
from app.models.user import User
from app.models.brand import Brand
from app.models.juice import Juice, JuiceStatus
from app.models.review import Review
from app.models.flavor_tag import FlavorTag, JuiceFlavorTag


def test_create_user() -> None:
    """测试创建用户模型"""
    user = User(username="test", email="test@test.com", hashed_password="hash")
    assert user.username == "test"
    assert user.is_admin is False
    assert user.is_active is True


def test_create_brand() -> None:
    """测试创建品牌模型"""
    brand = Brand(name="Test Brand", country="USA")
    assert brand.name == "Test Brand"
    assert brand.country == "USA"


def test_create_juice() -> None:
    """测试创建烟油模型"""
    juice = Juice(brand_id=1, name="Test Juice", status=JuiceStatus.PENDING)
    assert juice.name == "Test Juice"
    assert juice.avg_rating == 0.0
    assert juice.review_count == 0


def test_create_review() -> None:
    """测试创建评论模型"""
    review = Review(juice_id=1, user_id=1, rating=8, comment="不错")
    assert review.rating == 8
    assert 1 <= review.rating <= 10


def test_create_flavor_tag() -> None:
    """测试创建标签模型"""
    tag = FlavorTag(name="清新")
    assert tag.name == "清新"


def test_create_juice_flavor_tag() -> None:
    """测试创建烟油-标签关联"""
    link = JuiceFlavorTag(juice_id=1, tag_id=1)
    assert link.juice_id == 1
    assert link.tag_id == 1
