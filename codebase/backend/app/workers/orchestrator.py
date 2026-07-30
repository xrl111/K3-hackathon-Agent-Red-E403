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
            import os
            # Build correct path relative to the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            testcases_path = os.path.join(base_dir, "data _Red_Team", "pi_rag_security_checker_70_testcases_en.json")
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
                
                import requests
                from app.services.evaluator_svc import evaluate_with_llm_judge
                
                # Send HTTP POST to assessment.target_url
                target_url = assessment.target_url
                headers = {}
                # Handle OpenAI / Ollama generic chat completions format
                payload = {
                    "model": "llama3", # Default if Ollama
                    "messages": [{"role": "user", "content": prompt}],
                    "prompt": prompt, # For Ollama /api/generate fallback
                    "stream": False
                }
                
                try:
                    res = requests.post(target_url, json=payload, headers=headers, timeout=30)
                    res.raise_for_status()
                    data = res.json()
                    
                    # Extract response text (handle both /chat/completions and /api/generate)
                    if "choices" in data and len(data["choices"]) > 0:
                        model_response = data["choices"][0]["message"]["content"]
                    elif "response" in data:
                        model_response = data["response"]
                    else:
                        model_response = str(data)
                except Exception as e:
                    model_response = f"Failed to connect to target URL: {e}"
                
                # Evaluate using LLM Judge
                evaluator_pass = evaluate_with_llm_judge(prompt, model_response)

                trace = Trace(
                    assessment_id=assessment.id,
                    turn=index,
                    prompt_sent=prompt,
                    model_response=model_response,
                    evaluator_pass=evaluator_pass
                )
                session.add(trace)
                session.commit()
            
            # Mark as COMPLETED
            assessment.status = "COMPLETED"
            session.add(assessment)
            session.commit()
            print(f"Assessment {assessment_id} completed successfully with {len(test_cases)} cases.")

