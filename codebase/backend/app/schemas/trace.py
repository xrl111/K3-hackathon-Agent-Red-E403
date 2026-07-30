from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class RetrievedChunkItem(BaseModel):
    id: str
    score: Optional[float] = None
    text: Optional[str] = None
    is_poisoned: bool = False


class TraceCreate(BaseModel):
    assessment_id: str
    turn: int = 1
    prompt_sent: str
    retrieved_chunks: List[RetrievedChunkItem] = Field(default_factory=list)
    model_response: str
    evaluator_pass: bool = True


class TraceResponse(BaseModel):
    trace_id: str
    turn: int
    prompt: str
    retrieved_chunks: List[RetrievedChunkItem]
    response: str
    evaluator_pass: bool

    model_config = ConfigDict(from_attributes=True)


class TraceListResponse(BaseModel):
    page: int = 1
    total: int = 0
    traces: List[TraceResponse]
