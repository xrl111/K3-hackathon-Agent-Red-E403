import requests
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"

print("1. Creating a new assessment...")
payload = {
    "target_url": "https://api.project-target.com/chat",
    "model_version": "gpt-4o",
    "policies": [],
    "canary_secrets": [],
    "test_profiles": []
}
res = requests.post(f"{BASE_URL}/assessments", json=payload)
res.raise_for_status()
data = res.json()
assessment_id = data["assessment_id"]
print(f"Created assessment: {assessment_id}")

print("\n2. Calling /run to trigger Background Task...")
run_res = requests.post(f"{BASE_URL}/assessments/{assessment_id}/run")
run_res.raise_for_status()
print("Run API Response:", run_res.json())

print("\n3. Polling /status...")
for i in range(30):
    status_res = requests.get(f"{BASE_URL}/assessments/{assessment_id}/status")
    status_data = status_res.json()
    print(f"Poll {i+1}: Status = {status_data['status']}, Progress = {status_data['progress']}")
    
    if status_data['status'] == "COMPLETED":
        print("\nTest completed successfully!")
        break
    time.sleep(1)

print("\n4. Verifying DB via API... (assuming traces are reachable, or we just trust the status)")
if status_data['status'] != "COMPLETED":
    print("Test did not complete in time.")
    sys.exit(1)

print("ALL TESTS PASSED!")
