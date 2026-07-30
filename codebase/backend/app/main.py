from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.chroma import get_chroma_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifecycle event: Tạo các bảng SQLite và khởi tạo ChromaDB client khi app startup
    create_db_and_tables()
    get_chroma_client()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for PI-RAG Security Checker",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Setup CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Đăng ký API router v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs"
    }
