from fastapi import APIRouter, HTTPException, status
from app.schemas.rag import RagInjectRequest, RagInjectResponse
from app.services.chroma_svc import ChromaService

router = APIRouter()

@router.post(
    "/{assessment_id}/inject",
    response_model=RagInjectResponse,
    summary="Inject documents into RAG Sandbox (ChromaDB)",
)
async def inject_rag_documents(
    assessment_id: str,
    request: RagInjectRequest
):
    """
    Push a text corpus into a new ChromaDB collection for a specific assessment.
    Automatically splits into chunks and simulates poisoned documents.
    """
    try:
        response = ChromaService.inject_documents(assessment_id, request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to inject documents: {str(e)}"
        )
