import json
from typing import Optional
from sqlmodel import Session, select
from app.models.assessment import Assessment, AssessmentConfig
from app.schemas.assessment import AssessmentCreate, AssessmentResponse


class AssessmentService:
    @staticmethod
    def create_assessment(session: Session, payload: AssessmentCreate) -> Assessment:
        """Create a new Assessment and save associated AssessmentConfig in DB."""
        assessment = Assessment(
            target_url=payload.target_url,
            model=payload.model_version,
            scope=payload.scope or "FULL",
            status="CREATED",
        )
        session.add(assessment)
        session.commit()
        session.refresh(assessment)

        config = AssessmentConfig(
            assessment_id=assessment.id,
            policies=json.dumps(payload.policies, ensure_ascii=False),
            canary_secrets=json.dumps(payload.canary_secrets, ensure_ascii=False),
            test_profiles=json.dumps(payload.test_profiles, ensure_ascii=False),
        )
        session.add(config)
        session.commit()
        session.refresh(config)

        return assessment

    @staticmethod
    def get_assessment_by_id(session: Session, assessment_id: str) -> Optional[AssessmentResponse]:
        """Retrieve Assessment details along with deserialized AssessmentConfig."""
        statement = select(Assessment).where(Assessment.id == assessment_id)
        assessment = session.exec(statement).first()
        if not assessment:
            return None

        config_statement = select(AssessmentConfig).where(AssessmentConfig.assessment_id == assessment_id)
        config = session.exec(config_statement).first()

        policies = json.loads(config.policies) if config and config.policies else []
        canary_secrets = json.loads(config.canary_secrets) if config and config.canary_secrets else []
        test_profiles = json.loads(config.test_profiles) if config and config.test_profiles else []

        return AssessmentResponse(
            id=assessment.id,
            target_url=assessment.target_url,
            model=assessment.model,
            scope=assessment.scope,
            status=assessment.status,
            policies=policies,
            canary_secrets=canary_secrets,
            test_profiles=test_profiles,
        )
