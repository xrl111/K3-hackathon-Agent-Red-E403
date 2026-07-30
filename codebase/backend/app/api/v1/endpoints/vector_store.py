from fastapi import APIRouter, HTTPException, status
from app.schemas.vector_store import (
    AddDocumentsRequest,
    AddDocumentsResponse,
    CollectionListResponse,
    QueryRequest,
    QueryResponse,
    VectorStoreHealthResponse,
)
from app.services.vector_store import VectorStoreService

router = APIRouter()


@router.get("/health", response_model=VectorStoreHealthResponse, summary="Check Vector Store Health")
async def health_check():
    """Returns vector store connection status and collections count."""
    try:
        return VectorStoreService.health_check()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector store health check failed: {str(e)}"
        )


@router.get("/collections", response_model=CollectionListResponse, summary="List Collections")
async def list_collections():
    """List all available ChromaDB collections and document counts."""
    try:
        return VectorStoreService.list_collections()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list collections: {str(e)}"
        )


@router.post("/add", response_model=AddDocumentsResponse, summary="Add or Upsert Documents")
async def add_documents(request: AddDocumentsRequest):
    """Add or update documents into specified ChromaDB collection."""
    try:
        return VectorStoreService.add_documents(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add documents: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse, summary="Similarity Search")
async def query_documents(request: QueryRequest):
    """Perform similarity search on documents stored in ChromaDB."""
    try:
        return VectorStoreService.query(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query vector store: {str(e)}"
        )


@router.delete("/collections/{collection_name}", summary="Delete Collection")
async def delete_collection(collection_name: str):
    """Delete a collection by name."""
    try:
        VectorStoreService.delete_collection(collection_name)
        return {"status": "success", "message": f"Collection '{collection_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete collection '{collection_name}': {str(e)}"
        )
