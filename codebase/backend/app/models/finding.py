import uuid
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.assessment import Assessment
    from app.models.trace import Trace


class Finding(SQLModel, table=True):
    __tablename__ = "findings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    assessment_id: str = Field(foreign_key="assessments.id", index=True, nullable=False)
    trace_id: Optional[str] = Field(default=None, foreign_key="traces.id", index=True, nullable=True)
    severity: str = Field(default="MEDIUM", nullable=False, description="CRITICAL, HIGH, MEDIUM, LOW, INFO")
    type: str = Field(default="VULNERABILITY", nullable=False, description="RAG_POISONING, CANARY_LEAK, DIRECT_INJECTION")
    status: str = Field(default="OPEN", nullable=False, description="OPEN, CONFIRMED, FALSE_POSITIVE, MANUAL_VERIFICATION")
    human_reviewer_comment: Optional[str] = Field(default=None, nullable=True)
    remediation: Optional[str] = Field(default=None, nullable=True)

    # Relationships
    assessment: Optional["Assessment"] = Relationship(back_populates="findings")
    trace: Optional["Trace"] = Relationship(back_populates="findings")
