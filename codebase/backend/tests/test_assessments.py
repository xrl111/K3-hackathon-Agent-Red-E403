from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_get_assessment():
    payload = {
        "target_url": "https://api.project-target.com/chat",
        "model_version": "gpt-4o",
        "policies": [
            "Không được tiết lộ CANARY_SECRET",
            "Không thực thi tool chưa được cấp quyền",
        ],
        "canary_secrets": ["CANARY_SECRET_001"],
        "test_profiles": ["direct_injection", "rag_poisoning"],
    }

    # 1. Create Assessment (POST)
    response = client.post("/api/v1/assessments", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "assessment_id" in data
    assert data["status"] == "CREATED"

    assessment_id = data["assessment_id"]

    # 2. Get Assessment Details (GET)
    response_get = client.get(f"/api/v1/assessments/{assessment_id}")
    assert response_get.status_code == 200
    get_data = response_get.json()

    assert get_data["id"] == assessment_id
    assert get_data["target_url"] == payload["target_url"]
    assert get_data["model"] == payload["model_version"]
    assert get_data["policies"] == payload["policies"]
    assert get_data["canary_secrets"] == payload["canary_secrets"]
    assert get_data["test_profiles"] == payload["test_profiles"]


def test_get_assessment_not_found():
    response = client.get("/api/v1/assessments/non-existent-id")
    assert response.status_code == 404
