import time
import json
import os
import requests
from sqlmodel import Session, select
from app.core.database import engine
from app.models.assessment import Assessment
from app.models.trace import Trace
from app.models.finding import Finding
from app.services.evaluator_svc import evaluate_test_case

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
            # Build correct path relative to the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            testcases_path = os.path.join(base_dir, "data _Red_Team", "pi_rag_security_checker_70_testcases_en.json")
            try:
                with open(testcases_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    test_cases = data.get("test_cases", [])
                    canaries = data.get("canaries", [])
                    clean_corpus = data.get("clean_corpus", [])
                    poisoned_corpus = data.get("poisoned_corpus", [])
            except Exception as e:
                print(f"Orchestrator Error: Failed to load testcases file. {e}")
                assessment.status = "FAILED"
                session.add(assessment)
                session.commit()
                return
                
            from app.services.chroma_svc import ChromaService
            try:
                chroma_collection = ChromaService.inject_test_corpus(
                    assessment_id=assessment_id,
                    clean_docs=clean_corpus,
                    poisoned_docs=poisoned_corpus
                )
            except Exception as e:
                print(f"Orchestrator Error: Failed to inject RAG corpus. {e}")
                chroma_collection = None

            # Simulate processing test_cases
            for index, test_case in enumerate(test_cases, start=1):
                # Simulated delay (e.g. 0.1s to make 70 cases faster, or 0.5s)
                time.sleep(0.1)
                
                prompt = test_case.get("input", {}).get("prompt", "No prompt found")
                test_name = test_case.get("name", "Unknown test")
                test_id = test_case.get("id", "Unknown ID")
                
                # RAG Query Integration
                retrieved_chunks = []
                final_prompt = prompt
                if chroma_collection and test_case.get("category") in ["rag_instruction_poisoning", "rag_knowledge_poisoning", "combined_attack"]:
                    try:
                        results = chroma_collection.query(query_texts=[prompt], n_results=5)
                        if results and "documents" in results and results["documents"]:
                            docs = results["documents"][0]
                            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                            
                            for i, doc in enumerate(docs):
                                retrieved_chunks.append({
                                    "content": doc,
                                    "metadata": metas[i]
                                })
                        
                        context = "\n".join([c["content"] for c in retrieved_chunks])
                        final_prompt = f"Context:\n{context}\n\nUser Question:\n{prompt}"
                    except Exception as e:
                        print(f"RAG query error: {e}")
                
                # Send HTTP POST to assessment.target_url
                target_url = assessment.target_url
                headers = {}
                # Handle OpenAI / Ollama generic chat completions format
                payload = {
                    "model": "llama3", # Default if Ollama
                    "messages": [{"role": "user", "content": final_prompt}],
                    "prompt": final_prompt, # For Ollama /api/generate fallback
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
                
                # Evaluate using deterministic rules and LLM Judge
                eval_result = evaluate_test_case(prompt, model_response, test_case, canaries)

                trace = Trace(
                    assessment_id=assessment.id,
                    turn=index,
                    prompt_sent=final_prompt,
                    model_response=model_response,
                    evaluator_pass=eval_result.passed,
                    retrieved_chunks_json=json.dumps(retrieved_chunks, ensure_ascii=False)
                )
                session.add(trace)
                session.commit()
                session.refresh(trace)
                
                if not eval_result.passed:
                    finding = Finding(
                        assessment_id=assessment.id,
                        trace_id=trace.id,
                        severity=eval_result.severity,
                        type=eval_result.finding_type,
                        description=f"[{test_id}] {test_name}: {eval_result.reason}",
                        status="OPEN",
                        evaluator_reason=eval_result.reason,
                    )
                    session.add(finding)
                    session.commit()
            
            # Mark as COMPLETED
            assessment.status = "COMPLETED"
            session.add(assessment)
            session.commit()
            print(f"Assessment {assessment_id} completed successfully with {len(test_cases)} cases.")

