from fastapi import APIRouter
from app.api.v1.endpoints import assessments, health, vector_store, rag, runner, findings, report

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
api_router.include_router(runner.router, prefix="/assessments", tags=["Test Runner"])
api_router.include_router(findings.router, tags=["Findings"])
api_router.include_router(report.router, prefix="/assessments", tags=["Reporting"])
api_router.include_router(rag.router, prefix="/rag", tags=["RAG Sandbox"])
api_router.include_router(vector_store.router, prefix="/vector-store", tags=["Vector Store"])
