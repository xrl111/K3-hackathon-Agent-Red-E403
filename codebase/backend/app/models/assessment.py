import uuid
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.trace import Trace
    from app.models.finding import Finding


class Assessment(SQLModel, table=True):
    __tablename__ = "assessments"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    target_url: str = Field(nullable=False)
    model: str = Field(default="gpt-4o", nullable=False)
    scope: str = Field(default="FULL", nullable=False)
    status: str = Field(default="CREATED", nullable=False, index=True)
    executive_summary: Optional[str] = Field(default=None, nullable=True)

    # Relationships
    config: Optional["AssessmentConfig"] = Relationship(
        back_populates="assessment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "uselist": False}
    )
    traces: List["Trace"] = Relationship(
        back_populates="assessment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    findings: List["Finding"] = Relationship(
        back_populates="assessment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class AssessmentConfig(SQLModel, table=True):
    __tablename__ = "assessment_configs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    assessment_id: str = Field(foreign_key="assessments.id", unique=True, index=True, nullable=False)

    # JSON formatted strings for array data
    policies: str = Field(default="[]", description="JSON list of policies")
    canary_secrets: str = Field(default="[]", description="JSON list of canary secrets")
    test_profiles: str = Field(default="[]", description="JSON list of test profiles")
    custom_headers: str = Field(default="{}", description="JSON string of custom headers")

    # Relationship back to Assessment
    assessment: Optional[Assessment] = Relationship(back_populates="config")
