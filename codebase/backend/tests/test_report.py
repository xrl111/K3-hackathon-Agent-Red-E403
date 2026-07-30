import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

print("1. Creating a new assessment...")
payload = {
    "target_url": "https://api.test-report.com",
    "model_version": "gpt-4o"
}
res = requests.post(f"{BASE_URL}/assessments", json=payload)
res.raise_for_status()
assessment_id = res.json()["assessment_id"]
print(f"Created assessment: {assessment_id}")

print("\n2. Seeding dummy findings directly via DB session...")
from sqlmodel import Session
from app.core.database import engine
from app.models.finding import Finding

with Session(engine) as session:
    f1 = Finding(assessment_id=assessment_id, severity="CRITICAL", type="CANARY_LEAK")
    f2 = Finding(assessment_id=assessment_id, severity="HIGH", type="RAG_POISONING")
    f3 = Finding(assessment_id=assessment_id, severity="INFO", type="DIRECT_INJECTION")
    session.add_all([f1, f2, f3])
    session.commit()
    session.refresh(f1)
    finding_id = f1.id
print("Inserted 3 dummy findings.")

print("\n3. Testing GET /findings...")
res_f = requests.get(f"{BASE_URL}/assessments/{assessment_id}/findings")
res_f.raise_for_status()
findings_list = res_f.json()
print(f"Found {len(findings_list)} findings.")
assert len(findings_list) == 3

print(f"\n4. Testing PUT /findings/{finding_id}/status (Updating to CONFIRMED)...")
update_payload = {
    "status": "CONFIRMED",
    "human_reviewer_comment": "Verified by admin"
}
res_put = requests.put(f"{BASE_URL}/findings/{finding_id}/status", json=update_payload)
res_put.raise_for_status()
updated_finding = res_put.json()
print(f"Updated status: {updated_finding['status']}, Comment: {updated_finding['human_reviewer_comment']}")
assert updated_finding['status'] == "CONFIRMED"
assert updated_finding['human_reviewer_comment'] == "Verified by admin"

print(f"\n5. Testing GET /report...")
res_rep = requests.get(f"{BASE_URL}/assessments/{assessment_id}/report")
res_rep.raise_for_status()
report = res_rep.json()
print("Report output:", report)
# 1 Critical (20 pts), 1 High (10 pts) -> Score = 100 - 30 = 70 (CONDITIONAL GO)
assert report['readiness_score'] == 70
assert report['recommendation'] == "CONDITIONAL GO"
assert report['metrics']['total_critical'] == 1
assert report['metrics']['total_high'] == 1

print("\nALL REPORT & FINDINGS VALIDATIONS PASSED!")
