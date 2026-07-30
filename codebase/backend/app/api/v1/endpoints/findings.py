from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.finding import Finding
from app.schemas.finding import FindingResponse, FindingUpdateStatus

router = APIRouter()

@router.get(
    "/assessments/{assessment_id}/findings",
    response_model=List[FindingResponse],
    summary="Get findings for an assessment",
    tags=["Findings"]
)
async def get_assessment_findings(
    assessment_id: str,
    session: Session = Depends(get_session)
):
    """Lấy danh sách các lỗ hổng (Findings) mà hệ thống phát hiện cho một Assessment."""
    statement = select(Finding).where(Finding.assessment_id == assessment_id)
    findings = session.exec(statement).all()
    return findings


@router.put(
    "/findings/{finding_id}/status",
    response_model=FindingResponse,
    summary="Update finding status",
    tags=["Findings"]
)
async def update_finding_status(
    finding_id: str,
    payload: FindingUpdateStatus,
    session: Session = Depends(get_session)
):
    """Cập nhật trạng thái của Finding (Human Review)."""
    finding = session.get(Finding, finding_id)
    if not finding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finding with ID '{finding_id}' not found"
        )
    
    finding.status = payload.status
    if payload.human_reviewer_comment is not None:
        finding.human_reviewer_comment = payload.human_reviewer_comment
    if payload.remediation is not None:
        finding.remediation = payload.remediation
        
    session.add(finding)
    session.commit()
    session.refresh(finding)
    
    return finding
