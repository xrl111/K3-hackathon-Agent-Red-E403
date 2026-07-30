from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

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

MAX_PAYLOAD_SIZE = 5 * 1024 * 1024 # 5 MB

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method in ["POST", "PUT", "PATCH"]:
        if request.headers.get("content-length"):
            content_length = int(request.headers["content-length"])
            if content_length > MAX_PAYLOAD_SIZE:
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": "Payload too large. Maximum size is 5MB."}
                )
    return await call_next(request)

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
