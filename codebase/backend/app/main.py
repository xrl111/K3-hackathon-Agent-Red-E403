from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="K3 Hackathon API",
    description="Backend API for AI Features",
    version="1.0.0"
)

# Setup CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên giới hạn origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheckResponse(BaseModel):
    status: str
    message: str

@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    return HealthCheckResponse(
        status="ok",
        message="Backend is up and running!"
    )

# Thêm các router ở đây
# app.include_router(my_router, prefix="/api/v1")
