import time
import json
from sqlmodel import Session, select
from app.core.database import engine
from app.models.assessment import Assessment
from app.models.trace import Trace

class TestOrchestrator:
    @staticmethod
    def run_assessment(assessment_id: str):
        """
        Background task to simulate sending prompts from the JSON testcase file.
        Updates Assessment status and creates Traces.
        """
        with Session(engine) as session:
            # Update status to RUNNING
            statement = select(Assessment).where(Assessment.id == assessment_id)
            assessment = session.exec(statement).first()
            if not assessment:
                print(f"Orchestrator Error: Assessment {assessment_id} not found.")
                return

            assessment.status = "RUNNING"
            session.add(assessment)
            session.commit()

            # Load testcases from JSON file
            testcases_path = r"d:\VinAI\code\K3-hackathon-Agent-Red-E403\data _Red_Team\pi_rag_security_checker_70_testcases_en.json"
            try:
                with open(testcases_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    test_cases = data.get("test_cases", [])
            except Exception as e:
                print(f"Orchestrator Error: Failed to load testcases file. {e}")
                assessment.status = "FAILED"
                session.add(assessment)
                session.commit()
                return

            # Simulate processing test_cases
            for index, test_case in enumerate(test_cases, start=1):
                # Simulated delay (e.g. 0.1s to make 70 cases faster, or 0.5s)
                time.sleep(0.1)
                
                prompt = test_case.get("input", {}).get("prompt", "No prompt found")
                test_name = test_case.get("name", "Unknown test")
                test_id = test_case.get("id", "Unknown ID")
                
                # Create a Trace
                # In a real scenario, this would send an HTTP POST to `assessment.target_url`
                trace = Trace(
                    assessment_id=assessment.id,
                    turn=index,
                    prompt_sent=prompt,
                    model_response=f"Simulated response for test case: {test_name} ({test_id})",
                    evaluator_pass=True  # Simulated passing evaluator
                )
                session.add(trace)
                session.commit()
            
            # Mark as COMPLETED
            assessment.status = "COMPLETED"
            session.add(assessment)
            session.commit()
            print(f"Assessment {assessment_id} completed successfully with {len(test_cases)} cases.")

