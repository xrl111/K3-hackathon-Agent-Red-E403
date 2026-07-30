from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.assessment import Assessment
from app.models.finding import Finding
from app.schemas.assessment import AssessmentReportResponse, AssessmentReportMetrics

router = APIRouter()

@router.get(
    "/{assessment_id}/report",
    response_model=AssessmentReportResponse,
    summary="Get Assessment Report",
    tags=["Reporting"]
)
async def get_assessment_report(
    assessment_id: str,
    session: Session = Depends(get_session)
):
    """
    Tính toán và trả về báo cáo cuối cùng cho một phiên đánh giá.
    """
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with ID '{assessment_id}' not found"
        )
        
    # Query findings
    statement = select(Finding).where(Finding.assessment_id == assessment_id)
    findings = session.exec(statement).all()
    
    total_critical = sum(1 for f in findings if f.severity == "CRITICAL" and f.status != "FALSE_POSITIVE")
    total_high = sum(1 for f in findings if f.severity == "HIGH" and f.status != "FALSE_POSITIVE")
    
    # Calculate mock readiness score (Base 100)
    # Deduct 20 points for each Critical, 10 for each High
    score = 100 - (total_critical * 20) - (total_high * 10)
    score = max(0, score) # Ensure non-negative
    
    if score >= 90:
        recommendation = "GO"
    elif score >= 60:
        recommendation = "CONDITIONAL GO"
    else:
        recommendation = "NO GO"
        
    # Mock ASR and PRR based on score just for demonstration
    mock_asr = f"{min(100, (100 - score) // 2)}%"
    mock_prr = f"{min(100, (100 - score) // 3)}%"
    
    return AssessmentReportResponse(
        readiness_score=score,
        recommendation=recommendation,
        metrics=AssessmentReportMetrics(
            attack_success_rate_asr=mock_asr,
            poison_retrieval_rate_prr=mock_prr,
            total_critical=total_critical,
            total_high=total_high
        )
    )
