from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AssessmentCreate(BaseModel):
    target_url: str = Field(..., description="Target AI application endpoint URL")
    model_version: str = Field(default="gpt-4o", description="Target LLM model version", alias="model")
    scope: Optional[str] = Field(default="FULL", description="Testing scope")
    policies: List[str] = Field(default_factory=list, description="List of security/safety policies")
    canary_secrets: List[str] = Field(default_factory=list, description="List of canary tokens/secrets to track")
    test_profiles: List[str] = Field(default_factory=list, description="List of test profiles to execute")

    model_config = ConfigDict(populate_by_name=True)


class AssessmentCreateResponse(BaseModel):
    assessment_id: str
    status: str


class AssessmentConfigResponse(BaseModel):
    id: str
    assessment_id: str
    policies: List[str]
    canary_secrets: List[str]
    test_profiles: List[str]

    model_config = ConfigDict(from_attributes=True)


class AssessmentResponse(BaseModel):
    id: str
    target_url: str
    model: str
    scope: str
    status: str
    policies: Optional[List[str]] = Field(default_factory=list)
    canary_secrets: Optional[List[str]] = Field(default_factory=list)
    test_profiles: Optional[List[str]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class AssessmentStatusResponse(BaseModel):
    assessment_id: str
    status: str
    progress: Optional[str] = None
    current_phase: Optional[str] = None
    progress_percentage: int = 0
    completed_tests: int = 0
    total_tests: int = 70


class AssessmentReportMetrics(BaseModel):
    attack_success_rate_asr: str
    poison_retrieval_rate_prr: str
    total_tests_run: int
    total_critical: int
    total_high: int
    total_medium: int


class AssessmentReportResponse(BaseModel):
    readiness_score: int
    recommendation: str
    metrics: AssessmentReportMetrics
    radar_chart: dict

