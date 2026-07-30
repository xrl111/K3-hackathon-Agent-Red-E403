from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.assessment import Assessment
from app.models.trace import Trace
from app.schemas.assessment import AssessmentStatusResponse
from app.workers.orchestrator import TestOrchestrator

router = APIRouter()

@router.post(
    "/{assessment_id}/run",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger the AI Assessment Test Runner",
)
async def run_assessment(
    assessment_id: str,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """
    Kích hoạt Background Job để bắt đầu gửi Prompt.
    """
    # Verify assessment exists
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment '{assessment_id}' not found."
        )
    
    if assessment.status in ["RUNNING", "COMPLETED"]:
        return {"message": "Test is already running or completed", "job_id": None}

    # Start the worker in the background
    background_tasks.add_task(TestOrchestrator.run_assessment, assessment_id)
    return {"message": "Test started", "job_id": f"job-{assessment_id[:8]}"}


@router.get(
    "/{assessment_id}/status",
    response_model=AssessmentStatusResponse,
    summary="Check Assessment Test Progress",
)
async def get_assessment_status(
    assessment_id: str,
    session: Session = Depends(get_session)
):
    """
    API để Frontend polling xem tiến độ chạy test.
    """
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment '{assessment_id}' not found."
        )

    # Calculate progress based on traces count
    statement = select(Trace).where(Trace.assessment_id == assessment_id)
    traces = session.exec(statement).all()
    completed_turns = len(traces)
    total_turns = 5 # Updated for Agent max turns
    
    breached = any(not t.evaluator_pass for t in traces)
    
    current_phase = "Sending Prompts" if assessment.status == "RUNNING" else "Idle"
    if assessment.status == "COMPLETED":
        if breached:
            current_phase = "Completed - Target Breached"
        else:
            current_phase = "Completed - Target Secure"

    progress_percentage = int((completed_turns / total_turns) * 100) if total_turns > 0 else 0
    if assessment.status == "COMPLETED":
        progress_percentage = 100 # Fill the bar when finished

    return AssessmentStatusResponse(
        assessment_id=assessment.id,
        status=assessment.status,
        progress=progress_str,
        current_phase=current_phase,
        progress_percentage=progress_percentage,
        completed_tests=completed_turns,
        total_tests=total_turns
    )

@router.get(
    "/{assessment_id}/traces",
    summary="Get Assessment Traces",
)
async def get_assessment_traces(
    assessment_id: str,
    session: Session = Depends(get_session)
):
    """
    API để Frontend lấy danh sách traces.
    """
    statement = select(Trace).where(Trace.assessment_id == assessment_id)
    traces = session.exec(statement).all()
    return {"traces": traces}
