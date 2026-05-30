"""数据库连接和会话管理"""
from sqlmodel import SQLModel, Session, create_engine
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """初始化数据库，创建所有表"""
    from app.models import user, brand, juice, review, flavor_tag  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:  # pyright: ignore[reportInvalidTypeArguments]
    """获取数据库会话的依赖注入"""
    with Session(engine) as session:
        yield session
