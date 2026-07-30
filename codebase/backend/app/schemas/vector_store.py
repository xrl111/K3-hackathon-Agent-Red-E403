from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentItem(BaseModel):
    id: str = Field(..., description="Unique ID for the document")
    content: str = Field(..., description="Text content of the document")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata key-value pairs")


class AddDocumentsRequest(BaseModel):
    collection_name: Optional[str] = Field(default=None, description="Target collection name")
    documents: List[DocumentItem] = Field(..., description="List of documents to add or update")


class AddDocumentsResponse(BaseModel):
    status: str = "success"
    added_count: int
    collection_name: str


class QueryRequest(BaseModel):
    collection_name: Optional[str] = Field(default=None, description="Collection to query")
    query_texts: List[str] = Field(..., description="List of search query strings")
    n_results: int = Field(default=5, ge=1, le=100, description="Number of results to return")
    where: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filter conditions")


class QueryResultItem(BaseModel):
    id: str
    document: str
    metadata: Optional[Dict[str, Any]] = None
    distance: Optional[float] = None


class QueryResponse(BaseModel):
    collection_name: str
    results: List[List[QueryResultItem]]


class CollectionInfo(BaseModel):
    name: str
    count: int


class CollectionListResponse(BaseModel):
    collections: List[CollectionInfo]


class VectorStoreHealthResponse(BaseModel):
    status: str = "ok"
    mode: str
    persist_directory: Optional[str] = None
    collections_count: int
