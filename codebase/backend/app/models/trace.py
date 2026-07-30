import uuid
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.assessment import Assessment
    from app.models.finding import Finding


class Trace(SQLModel, table=True):
    __tablename__ = "traces"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    assessment_id: str = Field(foreign_key="assessments.id", index=True, nullable=False)
    turn: int = Field(default=1, nullable=False)
    prompt_sent: str = Field(nullable=False)
    retrieved_chunks_json: Optional[str] = Field(default="[]", description="JSON string storing retrieved chunks data")
    model_response: str = Field(default="", nullable=False)
    evaluator_pass: bool = Field(default=True, nullable=False)

    # Relationships
    assessment: Optional["Assessment"] = Relationship(back_populates="traces")
    findings: List["Finding"] = Relationship(
        back_populates="trace",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
