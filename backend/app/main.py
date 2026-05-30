"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routers import auth, tags, admin_tags, brands, admin_brands, upload, juices, admin_juices


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore[reportUnusedParameter]
    """应用生命周期管理"""
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(tags.router)
app.include_router(admin_tags.router)
app.include_router(brands.router)
app.include_router(admin_brands.router)
app.include_router(upload.router)
app.include_router(juices.router)
app.include_router(admin_juices.router)


@app.get("/api/health")
def health_check() -> dict:
    """健康检查"""
    return {"code": 0, "message": "ok", "data": None}
