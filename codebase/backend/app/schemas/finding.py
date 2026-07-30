from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class FindingCreate(BaseModel):
    assessment_id: str
    trace_id: Optional[str] = None
    severity: str = Field(default="MEDIUM", description="CRITICAL, HIGH, MEDIUM, LOW, INFO")
    type: str = Field(default="VULNERABILITY", description="RAG_POISONING, CANARY_LEAK, DIRECT_INJECTION")
    status: str = Field(default="OPEN", description="OPEN, CONFIRMED, FALSE_POSITIVE, MANUAL_VERIFICATION")
    description: str = Field(default="")
    evaluator_reason: Optional[str] = None
    human_reviewer_comment: Optional[str] = None
    remediation: Optional[str] = None


class FindingUpdateStatus(BaseModel):
    status: str = Field(..., description="CONFIRMED, FALSE_POSITIVE, MANUAL_VERIFICATION, OPEN")
    human_reviewer_comment: Optional[str] = None
    remediation: Optional[str] = None


class FindingResponse(BaseModel):
    id: str
    assessment_id: str
    trace_id: Optional[str] = None
    severity: str
    type: str
    description: str
    status: str
    evaluator_reason: Optional[str] = None
    human_reviewer_comment: Optional[str] = None
    remediation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FindingListResponse(BaseModel):
    findings: List[FindingResponse]
