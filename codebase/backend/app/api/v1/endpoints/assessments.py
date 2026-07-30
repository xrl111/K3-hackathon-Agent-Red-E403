from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.validators import validate_target_url

from app.core.database import get_session
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentCreateResponse,
    AssessmentResponse,
)
from app.services.assessment_svc import AssessmentService

router = APIRouter()


@router.post(
    "",
    response_model=AssessmentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Khởi tạo một phiên đánh giá mới",
)
async def create_assessment(
    payload: AssessmentCreate,
    session: Session = Depends(get_session),
):
    """Khởi tạo phiên đánh giá mới và lưu cấu hình vào database."""
    validate_target_url(payload.target_url)
    assessment = AssessmentService.create_assessment(session=session, payload=payload)
    return AssessmentCreateResponse(
        assessment_id=assessment.id,
        status=assessment.status,
    )


@router.get(
    "/export-dataset/jsonl",
    summary="Export successful attacks dataset in JSONL format",
)
async def export_dataset(session: Session = Depends(get_session)):
    """Xuất danh sách các lượt tấn công thành công dưới định dạng JSONL."""
    from fastapi.responses import StreamingResponse
    import io
    import json
    from sqlmodel import select
    from app.models.trace import Trace
    
    traces = session.exec(select(Trace).where(Trace.evaluator_pass == False)).all()
    
    output = io.StringIO()
    for trace in traces:
        entry = {
            "instruction": "Craft an attack to bypass the AI's defenses.",
            "input": trace.prompt_sent,
            "output": trace.model_response,
            "turn": trace.turn
        }
        output.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="application/jsonl",
        headers={"Content-Disposition": "attachment; filename=redteam_dataset.jsonl"}
    )

@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="Lấy chi tiết cấu hình phiên đánh giá",
)
async def get_assessment(
    assessment_id: str,
    session: Session = Depends(get_session),
):
    """Trả về chi tiết thông tin và cấu hình của phiên đánh giá theo ID."""
    result = AssessmentService.get_assessment_by_id(session=session, assessment_id=assessment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with ID '{assessment_id}' not found",
        )
    return result
