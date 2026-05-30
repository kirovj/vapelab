"""测试应用配置"""
from app.config import settings


def test_settings_defaults() -> None:
    """测试默认配置值"""
    assert settings.APP_NAME == "雾室 - vapelab"
    assert settings.DEBUG is True
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
