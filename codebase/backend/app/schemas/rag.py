from typing import List, Optional
from pydantic import BaseModel, Field

class RagInjectRequest(BaseModel):
    texts: List[str] = Field(..., description="Array of text documents to inject")
    chunk_size: Optional[int] = Field(default=500, description="Size of each text chunk")
    poison_ratio: Optional[float] = Field(default=0.1, description="Ratio of chunks to be marked as poisoned")

class RagInjectResponse(BaseModel):
    message: str
    total_chunks: int
    poisoned_chunks: int
    collection_name: str
