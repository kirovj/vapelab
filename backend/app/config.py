"""应用配置管理"""
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    # 数据库
    DATABASE_URL: str = "sqlite:///./vapelab.db"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 文件上传
    UPLOAD_DIR: str = str(Path(__file__).parent.parent / "static" / "uploads")
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # 应用
    APP_NAME: str = "雾室 - vapelab"
    DEBUG: bool = True

    model_config = ConfigDict(env_file=".env")


settings = Settings()
