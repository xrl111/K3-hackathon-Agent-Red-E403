from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    return HealthCheckResponse(
        status="ok",
        message="Backend is up and running!"
    )
